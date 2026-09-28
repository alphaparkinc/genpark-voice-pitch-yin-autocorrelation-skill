from client import VoicePitchYINEngine
import math

def main():
    yin = VoicePitchYINEngine(sample_rate=16000)
    test_freq = 220.0 # Concert A3
    signal = [0.8 * math.sin(2 * math.pi * test_freq * i / 16000) for i in range(1600)]
    res = yin.detect_pitch(signal)
    print("Voice Pitch YIN Verification:")
    print(f"Detected: {res['detected']}, Pitch: {res['pitch_hz']} Hz (Target: {test_freq} Hz)")
    print(f"Confidence: {res['harmonicity_confidence']}")

if __name__ == "__main__":
    main()
