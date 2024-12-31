"use client"
import React, { useState } from "react";

interface Color {
  id: number; // Add a unique identifier
  name: string;
  hex: string;
}

interface ColorWheelProps {
  onColorSelect: (color: Color) => void;
}

export function ColorWheel({ onColorSelect }: ColorWheelProps) {
  const [selectedColorId, setSelectedColorId] = useState<number | null>(null);

  // Generate 52 evenly spaced colors
  const generateColors = (count: number) => {
    const colors: Color[] = [];
    const baseColors = [
      "#FF0000", "#FF7F00", "#FFFF00", "#7FFF00", "#00FF00", "#00FF7F",
      "#00FFFF", "#007FFF", "#0000FF", "#7F00FF", "#FF00FF", "#FF007F",
    ]; // Base rainbow colors

    for (let i = 0; i < count; i++) {
      colors.push({
        id: i, // Assign a unique ID to each slice
        name: `Color ${i + 1}`,
        hex: baseColors[i % baseColors.length], // Cycle through base colors
      });
    }
    return colors;
  };

  const colors = generateColors(52);

  // Handle click events
  // good template for click
  const handleColorClick = (color: Color) => {
    setSelectedColorId(color.id); // Set the selected slice by ID
    onColorSelect(color); // Pass the selected color to the parent
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

          const isSelected = selectedColorId === color.id;

          return (
            <path
              key={color.id} // Use the unique ID as the key
              d={pathData}
              fill={color.hex}
              stroke={isSelected ? "#000" : "#fff"} // Apply black border if selected
              strokeWidth={isSelected ? 2 : 1}
              onClick={() => handleColorClick(color)} // Pass the entire color object
              style={{
                transition: "stroke-width 0.3s ease",
              }}
            />
          );
        })}
      </svg>
    </div>
  );
}