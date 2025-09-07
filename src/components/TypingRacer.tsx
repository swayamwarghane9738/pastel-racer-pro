import { useState, useEffect, useCallback, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Car } from "./Car";
import { ParticleSystem } from "./ParticleSystem";
import { useGameAudio } from "@/hooks/useGameAudio";
import { useToast } from "@/hooks/use-toast";

type GameState = "menu" | "playing" | "paused" | "finished";
type Difficulty = "easy" | "normal" | "hard";

interface GameStats {
  wpm: number;
  accuracy: number;
  score: number;
  wordsCompleted: number;
  timeRemaining: number;
}

const WORD_LISTS = {
  easy: [
    "cat", "dog", "sun", "run", "fun", "car", "big", "red", "hot", "cold",
    "yes", "no", "go", "up", "down", "happy", "fast", "slow", "good", "bad"
  ],
  normal: [
    "house", "water", "computer", "keyboard", "mouse", "typing", "racing", "speed",
    "challenge", "victory", "practice", "improve", "accuracy", "champion", "winner",
    "puzzle", "adventure", "journey", "explore", "discover", "create", "design"
  ],
  hard: [
    "extraordinary", "magnificent", "programming", "development", "architecture",
    "infrastructure", "optimization", "performance", "complexity", "algorithm", 
    "implementation", "visualization", "transformation", "revolutionary", 
    "technological", "sophisticated", "comprehensive", "responsibility"
  ]
};

const DIFFICULTY_SETTINGS = {
  easy: { timeLimit: 45, carSpeed: 0.8, wordDelay: 3000 },
  normal: { timeLimit: 60, carSpeed: 1.0, wordDelay: 2500 },
  hard: { timeLimit: 75, carSpeed: 1.2, wordDelay: 2000 }
};

export const TypingRacer = () => {
  const [gameState, setGameState] = useState<GameState>("menu");
  const [difficulty, setDifficulty] = useState<Difficulty>("normal");
  const [currentWord, setCurrentWord] = useState("");
  const [typedText, setTypedText] = useState("");
  const [carPosition, setCarPosition] = useState(0);
  const [stats, setStats] = useState<GameStats>({
    wpm: 0,
    accuracy: 100,
    score: 0,
    wordsCompleted: 0,
    timeRemaining: 60
  });
  
  const [startTime, setStartTime] = useState<number | null>(null);
  const [charactersTyped, setCharactersTyped] = useState(0);
  const [correctCharacters, setCorrectCharacters] = useState(0);
  const [particles, setParticles] = useState<Array<{id: string, x: number, y: number, type: "celebration" | "error" | "victory" | "sparkle"}>>([]);
  const [showCelebration, setShowCelebration] = useState(false);

  const gameContainerRef = useRef<HTMLDivElement>(null);
  const { playSound } = useGameAudio();
  const { toast } = useToast();

  // Generate random word based on difficulty
  const getRandomWord = useCallback(() => {
    const wordList = WORD_LISTS[difficulty];
    return wordList[Math.floor(Math.random() * wordList.length)];
  }, [difficulty]);

  // Start new game
  const startGame = useCallback(() => {
    const settings = DIFFICULTY_SETTINGS[difficulty];
    setGameState("playing");
    setCarPosition(0);
    setTypedText("");
    setCurrentWord(getRandomWord());
    setStartTime(Date.now());
    setCharactersTyped(0);
    setCorrectCharacters(0);
    setParticles([]);
    setShowCelebration(false);
    setStats({
      wpm: 0,
      accuracy: 100,
      score: 0,
      wordsCompleted: 0,
      timeRemaining: settings.timeLimit
    });
    
    // Focus the document to enable keyboard input
    document.body.focus();
    playSound("gameStart");
  }, [difficulty, getRandomWord, playSound]);

  // Complete current word
  const completeWord = useCallback(() => {
    const wordLength = currentWord.length;
    const baseScore = wordLength * 10;
    const timeBonus = Math.floor(stats.timeRemaining / 5);
    const accuracyBonus = Math.floor(stats.accuracy);
    const totalScore = baseScore + timeBonus + accuracyBonus;
    
    setStats(prev => ({
      ...prev,
      score: prev.score + totalScore,
      wordsCompleted: prev.wordsCompleted + 1
    }));
    
    // Move car forward
    const carAdvance = 0.15; // 15% per word
    setCarPosition(prev => Math.min(prev + carAdvance, 1));
    
    // Add celebration particles
    const newParticles: Array<{id: string, x: number, y: number, type: "celebration" | "error" | "victory" | "sparkle"}> = Array.from({ length: 6 }, (_, i) => ({
      id: `${Date.now()}-${i}`,
      x: Math.random() * 100,
      y: Math.random() * 50 + 25,
      type: "celebration" as const
    }));
    setParticles(prev => [...prev, ...newParticles]);
    
    // Clear particles after animation
    setTimeout(() => {
      setParticles(prev => prev.filter(p => !newParticles.find(np => np.id === p.id)));
    }, 2000);
    
    setTypedText("");
    setCurrentWord(getRandomWord());
    playSound("wordComplete");
    
    // Check win condition
    if (carPosition + carAdvance >= 1) {
      finishGame(true);
    }
  }, [currentWord, stats, carPosition, getRandomWord, playSound]);

  // Finish game
  const finishGame = useCallback((won: boolean = false) => {
    setGameState("finished");
    setShowCelebration(won);
    
    if (won) {
      playSound("victory");
      toast({
        title: "🏆 Congratulations!",
        description: `You won with ${stats.score} points!`,
      });
      
      // Add massive celebration
      const celebrationParticles: Array<{id: string, x: number, y: number, type: "celebration" | "error" | "victory" | "sparkle"}> = Array.from({ length: 20 }, (_, i) => ({
        id: `celebration-${Date.now()}-${i}`,
        x: Math.random() * 100,
        y: Math.random() * 100,
        type: "victory" as const
      }));
      setParticles(prev => [...prev, ...celebrationParticles]);
    } else {
      playSound("gameOver");
    }
  }, [stats.score, toast, playSound]);

  // Handle keyboard input
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (gameState !== "playing") return;
      
      if (e.key === "Backspace") {
        setTypedText(prev => prev.slice(0, -1));
        playSound("backspace");
        return;
      }
      
      if (e.key === "Escape") {
        setGameState("paused");
        return;
      }
      
      // Handle printable characters
      if (e.key.length === 1 && !e.ctrlKey && !e.altKey && !e.metaKey) {
        const char = e.key.toLowerCase();
        const targetChar = currentWord[typedText.length]?.toLowerCase();
        
        setCharactersTyped(prev => prev + 1);
        
        if (char === targetChar) {
          setCorrectCharacters(prev => prev + 1);
          setTypedText(prev => prev + char);
          playSound("correct");
          
          // Check if word is complete
          if (typedText + char === currentWord) {
            completeWord();
          }
        } else {
          playSound("error");
          // Add error effect
          const errorParticle: {id: string, x: number, y: number, type: "celebration" | "error" | "victory" | "sparkle"} = {
            id: `error-${Date.now()}`,
            x: Math.random() * 30 + 40,
            y: Math.random() * 20 + 40,
            type: "error" as const
          };
          setParticles(prev => [...prev, errorParticle]);
          
          setTimeout(() => {
            setParticles(prev => prev.filter(p => p.id !== errorParticle.id));
          }, 1000);
        }
      }
    };

    window.addEventListener("keydown", handleKeyPress);
    return () => window.removeEventListener("keydown", handleKeyPress);
  }, [gameState, currentWord, typedText, completeWord, playSound]);

  // Game timer and stats update
  useEffect(() => {
    if (gameState !== "playing" || !startTime) return;
    
    const timer = setInterval(() => {
      const elapsed = (Date.now() - startTime) / 1000;
      const timeLimit = DIFFICULTY_SETTINGS[difficulty].timeLimit;
      const timeRemaining = Math.max(timeLimit - elapsed, 0);
      
      // Calculate WPM (5 characters = 1 word)
      const wpm = charactersTyped > 0 ? (correctCharacters / 5) / (elapsed / 60) : 0;
      
      // Calculate accuracy
      const accuracy = charactersTyped > 0 ? (correctCharacters / charactersTyped) * 100 : 100;
      
      setStats(prev => ({
        ...prev,
        wpm: Math.round(wpm),
        accuracy: Math.round(accuracy),
        timeRemaining: Math.ceil(timeRemaining)
      }));
      
      // Check time limit
      if (timeRemaining <= 0) {
        finishGame(false);
      }
    }, 100);
    
    return () => clearInterval(timer);
  }, [gameState, startTime, difficulty, charactersTyped, correctCharacters, finishGame]);

  const renderTypingArea = () => {
    return (
      <Card className="game-card p-8 mb-6 relative overflow-hidden">
        <div className="text-center">
          <div className="text-6xl font-bold mb-4 font-mono tracking-wide">
            {currentWord.split("").map((char, index) => {
              const isTyped = index < typedText.length;
              const isCorrect = isTyped && typedText[index] === char;
              const isCurrent = index === typedText.length;
              
              return (
                <span
                  key={index}
                  className={`
                    ${isTyped 
                      ? isCorrect 
                        ? "typing-correct" 
                        : "typing-error"
                      : "text-muted-foreground"
                    }
                    ${isCurrent ? "bg-primary/20 animate-pulse" : ""}
                    transition-all duration-200
                  `}
                >
                  {char}
                </span>
              );
            })}
          </div>
          
          <div className="text-lg text-muted-foreground">
            Type the word above to move your car forward!
          </div>
        </div>
        
        <ParticleSystem particles={particles} />
      </Card>
    );
  };

  const renderGameStats = () => (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <Card className="p-4 text-center">
        <div className="text-2xl font-bold text-primary">{stats.wpm}</div>
        <div className="text-sm text-muted-foreground">WPM</div>
      </Card>
      <Card className="p-4 text-center">
        <div className="text-2xl font-bold text-secondary">{stats.accuracy}%</div>
        <div className="text-sm text-muted-foreground">Accuracy</div>
      </Card>
      <Card className="p-4 text-center">
        <div className="text-2xl font-bold text-accent">{stats.score.toLocaleString()}</div>
        <div className="text-sm text-muted-foreground">Score</div>
      </Card>
      <Card className="p-4 text-center">
        <div className="text-2xl font-bold text-primary">{stats.timeRemaining}s</div>
        <div className="text-sm text-muted-foreground">Time Left</div>
      </Card>
    </div>
  );

  const renderTrack = () => (
    <div className="relative mb-8">
      {/* Track */}
      <div className="h-24 bg-gradient-to-r from-game-track via-secondary/30 to-game-track rounded-2xl relative overflow-hidden border-4 border-border">
        {/* Track lines */}
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"></div>
        
        {/* Finish line */}
        <div className="absolute right-4 top-0 bottom-0 w-4 bg-gradient-to-b from-game-finish via-white to-game-finish rounded-full shadow-lg"></div>
        
        {/* Car */}
        <div 
          className="absolute top-1/2 transform -translate-y-1/2 transition-all duration-500 ease-out"
          style={{ left: `${carPosition * 85 + 5}%` }}
        >
          <Car isMoving={gameState === "playing"} />
        </div>
      </div>
      
      {/* Progress bar */}
      <Progress value={carPosition * 100} className="mt-4 h-3" />
      <div className="text-center mt-2 text-sm text-muted-foreground">
        Race Progress: {Math.round(carPosition * 100)}%
      </div>
    </div>
  );

  if (gameState === "menu") {
    return (
      <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-background via-muted/50 to-background">
        <Card className="game-card p-12 max-w-2xl w-full text-center animate-bounce-in">
          <div className="mb-8">
            <h1 className="text-6xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent mb-4">
              🏁 Typing Racer
            </h1>
            <p className="text-xl text-muted-foreground">
              Race to the finish line by typing words correctly!
            </p>
          </div>
          
          <div className="mb-8">
            <h3 className="text-lg font-semibold mb-4">Choose Difficulty:</h3>
            <div className="flex gap-4 justify-center">
              {(["easy", "normal", "hard"] as Difficulty[]).map((diff) => (
                <Button
                  key={diff}
                  variant={difficulty === diff ? "default" : "outline"}
                  onClick={() => setDifficulty(diff)}
                  className="capitalize"
                >
                  {diff}
                </Button>
              ))}
            </div>
          </div>
          
          <Button 
            onClick={startGame}
            size="lg" 
            className="game-button text-xl px-12 py-6"
          >
            🏎️ Start Racing!
          </Button>
          
          <div className="mt-8 text-sm text-muted-foreground space-y-2">
            <p>🎯 Type words to move your car forward</p>
            <p>⚡ Complete words quickly for bonus points</p>
            <p>🏆 Reach the finish line before time runs out!</p>
          </div>
        </Card>
      </div>
    );
  }

  if (gameState === "paused") {
    return (
      <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-background via-muted/50 to-background">
        <Card className="game-card p-8 max-w-md w-full text-center">
          <h2 className="text-3xl font-bold mb-4">⏸️ Paused</h2>
          <p className="text-muted-foreground mb-6">Game paused. Ready to continue?</p>
          <div className="space-y-3">
            <Button onClick={() => setGameState("playing")} className="w-full">
              Resume Game
            </Button>
            <Button onClick={() => setGameState("menu")} variant="outline" className="w-full">
              Back to Menu
            </Button>
          </div>
        </Card>
      </div>
    );
  }

  if (gameState === "finished") {
    return (
      <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-background via-muted/50 to-background">
        <Card className="game-card p-12 max-w-2xl w-full text-center relative overflow-hidden">
          {showCelebration && <ParticleSystem particles={particles} />}
          
          <div className="mb-8">
            <h2 className="text-5xl font-bold mb-4">
              {showCelebration ? "🏆 Victory!" : "⏰ Time's Up!"}
            </h2>
            <p className="text-xl text-muted-foreground">
              {showCelebration 
                ? "Congratulations! You reached the finish line!"
                : "Great effort! Try again to improve your time!"
              }
            </p>
          </div>
          
          <div className="grid grid-cols-2 gap-4 mb-8">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">{stats.score.toLocaleString()}</div>
              <div className="text-sm text-muted-foreground">Final Score</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-secondary">{stats.wpm}</div>
              <div className="text-sm text-muted-foreground">Words Per Minute</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-accent">{stats.accuracy}%</div>
              <div className="text-sm text-muted-foreground">Accuracy</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">{stats.wordsCompleted}</div>
              <div className="text-sm text-muted-foreground">Words Completed</div>
            </div>
          </div>
          
          <div className="space-y-3">
            <Button onClick={startGame} className="game-button w-full text-lg">
              🔄 Race Again
            </Button>
            <Button onClick={() => setGameState("menu")} variant="outline" className="w-full">
              Back to Menu
            </Button>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div 
      ref={gameContainerRef}
      className="min-h-screen p-4 bg-gradient-to-br from-background via-muted/50 to-background"
      tabIndex={0}
    >
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <Badge variant="outline" className="text-lg px-4 py-2">
            {difficulty.toUpperCase()} MODE
          </Badge>
          <Button 
            variant="outline" 
            onClick={() => setGameState("paused")}
            className="px-6"
          >
            ⏸️ Pause
          </Button>
        </div>
        
        {renderGameStats()}
        {renderTrack()}
        {renderTypingArea()}
        
        <div className="text-center text-sm text-muted-foreground">
          Press ESC to pause • Type to move your car • Reach the finish line to win!
        </div>
      </div>
    </div>
  );
};