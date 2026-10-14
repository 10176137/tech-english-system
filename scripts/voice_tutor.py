"""
Voice Tutor Pipeline (本地开源语音私教流水线)
- 耳朵 (STT): Systran/faster-distil-whisper-small.en (CPU 极速版)
- 门禁 (VAD): Silero VAD (免按键智能断句)
- 大脑 (LLM): 智谱 GLM-4 (通过 API)
- 嘴巴 (TTS): hexgrad/Kokoro-82M (开源高质美音)
- 联动: 自动将纠错沉淀至 ledger/error-ledger.md
"""

import os
import re
import sys
import time
import queue
import numpy as np
import sounddevice as sd
import soundfile as sf
import torch
from faster_whisper import WhisperModel
from kokoro import KPipeline
from zhipuai import ZhipuAI

# ==================== 1. 配置项 ====================
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")
SAMPLE_RATE = 16000
VAD_CONFIRMATION_THRESHOLD = 0.5
SILENCE_DURATION_THRESHOLD = 0.8  # 停顿超过 0.8s 自动判定讲完
LEDGER_PATH = os.path.join(os.path.dirname(__file__), "../ledger/error-ledger.md")
LESSON_PATH = os.path.join(os.path.dirname(__file__), "../current_lesson.txt")

# ==================== 2. 模型初始化 ====================
print("=" * 60)
print("🚀 正在加载本地开源语音流水线 (纯 CPU 极速驱动)...")
print("=" * 60)

# 加载 Silero VAD
print("[1/3] 正在加载 Silero VAD 静音检测器...")
vad_model, vad_utils = torch.hub.load(
    repo_or_dir='snakers4/silero-vad',
    model='silero_vad',
    force_reload=False,
    onnx=False
)
(get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = vad_utils

# 加载 Distil-Whisper
print("[2/3] 正在加载本地耳朵: Distil-Whisper (small.en)...")
whisper = WhisperModel("distil-small.en", device="cpu", compute_type="int8")

# 加载 Kokoro-82M
print("[3/3] 正在加载本地嘴巴: Kokoro-82M (美式英语)...")
tts_pipeline = KPipeline(lang_code='a')

# 智谱客户端
if not ZHIPU_API_KEY:
    print("\n⚠️ 提示: 未检测到 ZHIPU_API_KEY 环境变量，请在终端设置或在代码中指定。")
client = ZhipuAI(api_key=ZHIPU_API_KEY or "your_zhipu_api_key_here")

# ==================== 3. 核心工具函数 ====================
def read_current_lesson():
    """读取当前 Empower 课程上下文"""
    if os.path.exists(LESSON_PATH):
        try:
            with open(LESSON_PATH, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return f"\n[Current Empower Lesson Context]:\n{content}\n"
        except Exception:
            pass
    return ""

def append_error_to_ledger(bug_info):
    """自动将语法 Bug 写入 Git 错题本"""
    if not os.path.exists(LEDGER_PATH):
        return
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n---\n\n### Oral Bug [{timestamp}]\n* {bug_info}\n"
    try:
        with open(LEDGER_PATH, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"📁 已自动记录至错题本: {LEDGER_PATH}")
    except Exception as e:
        print(f"写入错题本失败: {e}")

def record_audio_vad():
    """使用 Silero VAD 实现免按键自动拾音"""
    print("\n🟢 [Listening] 请直接开口说话 (说完停顿 0.8s 自动提交)...")
    q = queue.Queue()

    def audio_callback(indata, frames, time_info, status):
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())

    audio_frames = []
    speaking = False
    silence_start = None
    CHUNK = 512  # Silero 推荐的 16kHz 分块
    
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32', blocksize=CHUNK, callback=audio_callback):
        while True:
            chunk = q.get()
            audio_frames.append(chunk)
            tensor_chunk = torch.from_numpy(chunk.squeeze())
            speech_prob = vad_model(tensor_chunk, SAMPLE_RATE).item()

            if speech_prob > VAD_CONFIRMATION_THRESHOLD:
                if not speaking:
                    speaking = True
                    print("🎙️ 检测到语音输入中...")
                silence_start = None
            else:
                if speaking:
                    if silence_start is None:
                        silence_start = time.time()
                    elif time.time() - silence_start > SILENCE_DURATION_THRESHOLD:
                        # 超过静音阈值，判定说话结束
                        break
    
    concatenated = np.concatenate(audio_frames, axis=0).squeeze()
    return concatenated

def transcribe(audio_data):
    """Whisper 转写"""
    segments, _ = whisper.transcribe(audio_data, language="en")
    return " ".join([seg.text for seg in segments]).strip()

def ask_glm_tutor(user_text, lesson_context):
    """调用智谱 GLM-4 教学大脑"""
    system_prompt = f"""
You are an expert native English coach assisting a Chinese software engineer studying Cambridge English Empower.
{lesson_context}

RULES:
1. Speak in natural, concise spoken English (1-2 sentences at a time).
2. Keep the conversational ball rolling by asking a relevant question or prompting the next exercise.
3. If the user's sentence has a grammar, vocabulary, or pronunciation bug, format it at the beginning as:
   [BUG: <brief explanation of the error and the native correction>]
   Then continue your spoken response naturally.
"""
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ]
    )
    return response.choices[0].message.content

def speak_kokoro(text):
    """Kokoro-82M 语音合成并播放"""
    # 过滤掉 [BUG: ...] 诊断标记，不念给耳朵听
    spoken_text = re.sub(r'\[BUG:.*?\]', '', text).strip()
    if not spoken_text:
        return
    generator = tts_pipeline(spoken_text, voice='af_bella', speed=1.0)
    for _, _, audio in generator:
        sd.play(audio, 24000)
        sd.wait()

# ==================== 4. 主循环 ====================
def main():
    lesson_context = read_current_lesson()
    if lesson_context:
        print("📖 已加载 Empower 课本文本上下文。")
    else:
        print("ℹ️ 提示: 可在根目录创建 current_lesson.txt 粘贴今天学的课文内容。")

    print("\n🎧 请戴好耳机，系统已就绪！(按 Ctrl+C 退出)")
    
    while True:
        try:
            audio_data = record_audio_vad()
            user_text = transcribe(audio_data)
            
            if not user_text or len(user_text.strip()) < 2:
                continue
                
            print(f"\n👤 [You Said]: {user_text}")
            
            # 大脑思考
            ai_reply = ask_glm_tutor(user_text, lesson_context)
            
            # 解析诊断信息
            bug_match = re.search(r'\[BUG:(.*?)\]', ai_reply)
            if bug_match:
                bug_detail = bug_match.group(1).strip()
                print(f"🟡 [Grammar/Usage Fix]: {bug_detail}")
                append_error_to_ledger(f"Original: `{user_text}`\n  * Feedback: {bug_detail}")
                
            spoken_part = re.sub(r'\[BUG:.*?\]', '', ai_reply).strip()
            print(f"🤖 [Coach]: {spoken_part}")
            
            # 嘴巴发音
            speak_kokoro(spoken_part)
            
        except KeyboardInterrupt:
            print("\n👋 语音私教已安全退出。")
            break
        except Exception as e:
            print(f"\n❌ 运行异常: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
