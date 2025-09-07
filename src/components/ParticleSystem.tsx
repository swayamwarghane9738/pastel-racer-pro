import { useEffect, useState } from "react";

interface Particle {
  id: string;
  x: number;
  y: number;
  type: "celebration" | "error" | "victory" | "sparkle";
}

interface ParticleSystemProps {
  particles: Particle[];
}

const ParticleComponent: React.FC<{ particle: Particle }> = ({ particle }) => {
  const [opacity, setOpacity] = useState(1);
  const [scale, setScale] = useState(1);
  const [translateY, setTranslateY] = useState(0);

  useEffect(() => {
    const animationDuration = particle.type === "victory" ? 3000 : 2000;
    
    const animate = () => {
      const startTime = Date.now();
      
      const updateAnimation = () => {
        const elapsed = Date.now() - startTime;
        const progress = elapsed / animationDuration;
        
        if (progress >= 1) {
          setOpacity(0);
          return;
        }
        
        // Different animations for different particle types
        switch (particle.type) {
          case "celebration":
            setOpacity(1 - progress);
            setTranslateY(-progress * 50);
            setScale(1 - progress * 0.5);
            break;
            
          case "error":
            setOpacity(1 - progress);
            setScale(1 + Math.sin(progress * Math.PI * 4) * 0.1);
            break;
            
          case "victory":
            setOpacity(1 - progress * 0.8);
            setTranslateY(-progress * 100);
            setScale(1 + progress * 0.5);
            break;
            
          case "sparkle":
            setOpacity(Math.sin(progress * Math.PI));
            setScale(1 + Math.sin(progress * Math.PI * 2) * 0.3);
            break;
        }
        
        requestAnimationFrame(updateAnimation);
      };
      
      updateAnimation();
    };
    
    animate();
  }, [particle]);

  const getParticleStyle = () => {
    const baseClasses = "absolute pointer-events-none transition-all duration-100";
    
    switch (particle.type) {
      case "celebration":
        return `${baseClasses} w-3 h-3 bg-gradient-to-r from-yellow-400 to-orange-400 rounded-full`;
      case "error":
        return `${baseClasses} w-2 h-2 bg-gradient-to-r from-red-400 to-pink-400 rounded-full`;
      case "victory":
        return `${baseClasses} w-4 h-4 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full`;
      case "sparkle":
        return `${baseClasses} w-1 h-1 bg-yellow-300 rounded-full`;
      default:
        return `${baseClasses} w-2 h-2 bg-primary rounded-full`;
    }
  };

  const getParticleIcon = () => {
    switch (particle.type) {
      case "celebration":
        return "🎉";
      case "error":
        return "❌";
      case "victory":
        return "🏆";
      case "sparkle":
        return "✨";
      default:
        return "";
    }
  };

  return (
    <div
      className={getParticleStyle()}
      style={{
        left: `${particle.x}%`,
        top: `${particle.y}%`,
        opacity,
        transform: `scale(${scale}) translateY(${translateY}px)`,
      }}
    >
      {particle.type === "victory" && (
        <span className="absolute inset-0 flex items-center justify-center text-xs">
          {getParticleIcon()}
        </span>
      )}
      
      {particle.type === "celebration" && (
        <div className="absolute inset-0 animate-spin">
          <div className="w-full h-full bg-gradient-to-r from-yellow-400 to-orange-400 rounded-full"></div>
        </div>
      )}
      
      {particle.type === "error" && (
        <div className="absolute inset-0 animate-pulse">
          <div className="w-full h-full bg-red-400 rounded-full"></div>
        </div>
      )}
      
      {particle.type === "sparkle" && (
        <div className="absolute inset-0 animate-ping">
          <div className="w-full h-full bg-yellow-300 rounded-full"></div>
        </div>
      )}
    </div>
  );
};

export const ParticleSystem: React.FC<ParticleSystemProps> = ({ particles }) => {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map((particle) => (
        <ParticleComponent key={particle.id} particle={particle} />
      ))}
    </div>
  );
};

// Utility function to create particles
export const createParticles = (
  count: number, 
  type: Particle["type"], 
  centerX: number = 50, 
  centerY: number = 50,
  spread: number = 20
): Particle[] => {
  return Array.from({ length: count }, (_, i) => ({
    id: `${type}-${Date.now()}-${i}`,
    x: centerX + (Math.random() - 0.5) * spread,
    y: centerY + (Math.random() - 0.5) * spread,
    type
  }));
};