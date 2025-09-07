import { useEffect, useState } from "react";

interface CarProps {
  isMoving?: boolean;
  color?: "blue" | "green" | "red" | "purple";
}

export const Car: React.FC<CarProps> = ({ isMoving = false, color = "blue" }) => {
  const [bounce, setBounce] = useState(0);
  
  useEffect(() => {
    if (!isMoving) return;
    
    const interval = setInterval(() => {
      setBounce(prev => (prev + 1) % 4);
    }, 150);
    
    return () => clearInterval(interval);
  }, [isMoving]);

  const getCarColor = (colorName: string) => {
    const colors = {
      blue: "from-game-car-blue to-blue-300",
      green: "from-game-car-green to-green-300", 
      red: "from-red-300 to-red-400",
      purple: "from-purple-300 to-purple-400"
    };
    return colors[colorName as keyof typeof colors] || colors.blue;
  };

  return (
    <div className={`relative w-16 h-10 ${isMoving ? "car-style" : ""}`}>
      {/* Car shadow */}
      <div className="absolute -bottom-1 left-1 w-16 h-3 bg-game-shadow/30 rounded-full blur-sm"></div>
      
      {/* Main car body */}
      <div className={`
        relative w-14 h-8 bg-gradient-to-r ${getCarColor(color)}
        rounded-2xl border-2 border-white shadow-lg
        ${bounce % 2 === 0 && isMoving ? "animate-pulse" : ""}
        transition-all duration-200
      `}>
        {/* Car roof */}
        <div className="absolute top-1 left-2 w-10 h-4 bg-gradient-to-r from-white/40 to-white/20 rounded-xl border border-white/30"></div>
        
        {/* Headlights */}
        <div className="absolute -right-1 top-2 w-2 h-1 bg-yellow-200 rounded-full shadow-sm"></div>
        <div className="absolute -right-1 bottom-2 w-2 h-1 bg-red-300 rounded-full shadow-sm"></div>
        
        {/* Cute eyes */}
        <div className="absolute top-2 left-3 flex space-x-2">
          <div className="w-2 h-2 bg-white rounded-full flex items-center justify-center">
            <div className="w-1 h-1 bg-gray-800 rounded-full"></div>
          </div>
          <div className="w-2 h-2 bg-white rounded-full flex items-center justify-center">
            <div className="w-1 h-1 bg-gray-800 rounded-full"></div>
          </div>
        </div>
        
        {/* Happy mouth when moving */}
        {isMoving && (
          <div className="absolute top-4 left-4 w-3 h-1">
            <div className="w-full h-full border-b-2 border-gray-800 rounded-b-full"></div>
          </div>
        )}
      </div>
      
      {/* Wheels */}
      <div className="absolute -bottom-1 left-0 w-3 h-3 bg-gray-800 rounded-full border-2 border-gray-600 shadow-sm">
        <div className="absolute inset-1 bg-gray-600 rounded-full"></div>
      </div>
      <div className="absolute -bottom-1 right-0 w-3 h-3 bg-gray-800 rounded-full border-2 border-gray-600 shadow-sm">
        <div className="absolute inset-1 bg-gray-600 rounded-full"></div>
      </div>
      
      {/* Speed lines when moving */}
      {isMoving && (
        <div className="absolute right-16 top-1/2 transform -translate-y-1/2 opacity-60">
          {[...Array(3)].map((_, i) => (
            <div 
              key={i}
              className="w-6 h-0.5 bg-primary/40 rounded-full mb-1 animate-pulse"
              style={{ 
                animationDelay: `${i * 0.1}s`,
                width: `${20 - i * 4}px`
              }}
            ></div>
          ))}
        </div>
      )}
      
      {/* Sparkles when moving fast */}
      {isMoving && (
        <div className="absolute -top-2 -right-2">
          <div className="w-1 h-1 bg-yellow-400 rounded-full animate-ping"></div>
        </div>
      )}
    </div>
  );
};