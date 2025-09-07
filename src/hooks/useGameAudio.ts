import { useCallback, useRef, useEffect } from "react";

type SoundType = 
  | "correct" 
  | "error" 
  | "wordComplete" 
  | "gameStart" 
  | "victory" 
  | "gameOver" 
  | "backspace" 
  | "click";

interface AudioConfig {
  volume: number;
  enabled: boolean;
}

export const useGameAudio = (config: AudioConfig = { volume: 0.3, enabled: true }) => {
  const audioContextRef = useRef<AudioContext | null>(null);
  const gainNodeRef = useRef<GainNode | null>(null);

  // Initialize Web Audio API
  useEffect(() => {
    if (!config.enabled) return;

    const initAudio = async () => {
      try {
        const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
        const gainNode = audioContext.createGain();
        gainNode.connect(audioContext.destination);
        gainNode.gain.value = config.volume;

        audioContextRef.current = audioContext;
        gainNodeRef.current = gainNode;
      } catch (error) {
        console.warn("Web Audio API not supported:", error);
      }
    };

    initAudio();

    return () => {
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
    };
  }, [config.enabled, config.volume]);

  // Generate sound using oscillator
  const generateTone = useCallback((
    frequency: number,
    duration: number,
    type: OscillatorType = "sine",
    volume: number = 1
  ) => {
    if (!audioContextRef.current || !gainNodeRef.current || !config.enabled) return;

    const audioContext = audioContextRef.current;
    const gainNode = gainNodeRef.current;

    try {
      const oscillator = audioContext.createOscillator();
      const noteGain = audioContext.createGain();

      oscillator.connect(noteGain);
      noteGain.connect(gainNode);

      oscillator.frequency.value = frequency;
      oscillator.type = type;

      // Envelope for smooth sound
      const now = audioContext.currentTime;
      noteGain.gain.setValueAtTime(0, now);
      noteGain.gain.linearRampToValueAtTime(volume, now + 0.01);
      noteGain.gain.exponentialRampToValueAtTime(0.001, now + duration);

      oscillator.start(now);
      oscillator.stop(now + duration);
    } catch (error) {
      console.warn("Error generating tone:", error);
    }
  }, [config.enabled]);

  // Play different game sounds
  const playSound = useCallback((soundType: SoundType) => {
    switch (soundType) {
      case "correct":
        generateTone(440, 0.1, "sine", 0.3); // Pleasant beep
        break;
        
      case "error":
        generateTone(220, 0.2, "sawtooth", 0.2); // Lower, harsh sound
        break;
        
      case "wordComplete":
        // Quick ascending melody
        setTimeout(() => generateTone(440, 0.1, "sine", 0.3), 0);
        setTimeout(() => generateTone(554, 0.1, "sine", 0.3), 100);
        setTimeout(() => generateTone(659, 0.2, "sine", 0.3), 200);
        break;
        
      case "gameStart":
        // Uplifting start sound
        setTimeout(() => generateTone(330, 0.15, "sine", 0.4), 0);
        setTimeout(() => generateTone(440, 0.15, "sine", 0.4), 150);
        setTimeout(() => generateTone(550, 0.2, "sine", 0.4), 300);
        break;
        
      case "victory":
        // Victory fanfare
        const victoryNotes = [440, 554, 659, 880];
        victoryNotes.forEach((note, index) => {
          setTimeout(() => generateTone(note, 0.3, "sine", 0.5), index * 200);
        });
        break;
        
      case "gameOver":
        // Descending sad sound
        setTimeout(() => generateTone(440, 0.2, "sine", 0.3), 0);
        setTimeout(() => generateTone(330, 0.2, "sine", 0.3), 200);
        setTimeout(() => generateTone(220, 0.4, "sine", 0.3), 400);
        break;
        
      case "backspace":
        generateTone(800, 0.05, "square", 0.15); // Quick high click
        break;
        
      case "click":
        generateTone(1000, 0.03, "square", 0.1); // Very short click
        break;
        
      default:
        console.warn(`Unknown sound type: ${soundType}`);
    }
  }, [generateTone]);

  // Play chord (multiple notes at once)
  const playChord = useCallback((frequencies: number[], duration: number = 0.5) => {
    frequencies.forEach(freq => {
      generateTone(freq, duration, "sine", 0.2);
    });
  }, [generateTone]);

  // Play melody (notes in sequence)
  const playMelody = useCallback((
    notes: Array<{ frequency: number; duration: number }>,
    tempo: number = 1
  ) => {
    let currentTime = 0;
    notes.forEach(note => {
      setTimeout(() => {
        generateTone(note.frequency, note.duration, "sine", 0.3);
      }, currentTime * tempo);
      currentTime += note.duration * 1000;
    });
  }, [generateTone]);

  return {
    playSound,
    playChord,
    playMelody,
    isEnabled: config.enabled
  };
};