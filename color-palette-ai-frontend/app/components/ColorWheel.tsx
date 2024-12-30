"use client"
import React, { useState } from "react";

interface Color {
  name: string;
  hex: string;
}

interface ColorWheelProps {
  onColorSelect: (color: Color) => void;
}

export function ColorWheel({ onColorSelect }: ColorWheelProps) {
  const [selectedColor, setSelectedColor] = useState<Color | null>(null);

  // Generate 52 evenly spaced colors
  const generateColors = (count: number) => {
    const colors: Color[] = [];
    const baseColors = [
      "#FF0000", "#FF7F00", "#FFFF00", "#7FFF00", "#00FF00", "#00FF7F",
      "#00FFFF", "#007FFF", "#0000FF", "#7F00FF", "#FF00FF", "#FF007F",
    ]; // Base rainbow colors

    for (let i = 0; i < count; i++) {
      colors.push({
        name: `Color ${i + 1}`,
        hex: baseColors[i % baseColors.length], // Cycle through base colors
      });
    }
    return colors;
  };

  const colors = generateColors(52);

  // Handle click events
  const handleColorClick = (color: Color) => {
    setSelectedColor(color);
    onColorSelect(color);
  };

  return (
    <div className="relative w-[420px] h-[420px] mx-auto">
      <svg
        className="w-full h-full"
        viewBox="0 0 100 100"
        xmlns="http://www.w3.org/2000/svg"
        style={{ transform: "rotate(-90deg)" }}
      >
        {colors.map((color, index) => {
          const startAngle = (index / colors.length) * 2 * Math.PI;
          const endAngle = ((index + 1) / colors.length) * 2 * Math.PI;

          const largeArcFlag = endAngle - startAngle > Math.PI ? 1 : 0;

          const x1 = 50 + 50 * Math.cos(startAngle);
          const y1 = 50 + 50 * Math.sin(startAngle);
          const x2 = 50 + 50 * Math.cos(endAngle);
          const y2 = 50 + 50 * Math.sin(endAngle);

          const pathData = `
            M 50 50
            L ${x1} ${y1}
            A 50 50 0 ${largeArcFlag} 1 ${x2} ${y2}
            Z
          `;

          const isSelected = selectedColor?.hex === color.hex;

          // Calculate the "jutting out" effect
          const translateX = isSelected ? 5 * Math.cos((startAngle + endAngle) / 2) : 0;
          const translateY = isSelected ? 5 * Math.sin((startAngle + endAngle) / 2) : 0;

          return (
            <path
              key={color.name}
              d={pathData}
              fill={color.hex}
              stroke={isSelected ? "#000" : "#fff"}
              strokeWidth={isSelected ? 2 : 1}
              onClick={() => handleColorClick(color)}
              style={{
                transition: "transform 0.3s ease, translate 0.3s ease",
                transform: isSelected
                  ? `scale(1.25) translate(${translateX}px, ${translateY}px)`
                  : "scale(1) translate(0, 0)",
              }}
            />
          );
        })}
      </svg>
    </div>
  );
}
