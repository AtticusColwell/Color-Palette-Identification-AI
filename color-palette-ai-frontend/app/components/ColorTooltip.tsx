import React from "react";

interface ColorTooltipProps {
  color: {
    name: string;
    hex: string;
  };
  position: {
    x: number;
    y: number;
  };
}

export function ColorTooltip({ color, position }: ColorTooltipProps) {
  return (
    <div
      className="fixed z-50 bg-white rounded-lg shadow-lg p-3 pointer-events-none"
      style={{
        left: position.x + 10,
        top: position.y + 10,
      }}
    >
      <div className="flex flex-col gap-1">
        <div className="text-sm font-medium">{color.name}</div>
        <div className="text-xs text-gray-500">{color.hex}</div>
        <div
          className="w-full h-4 rounded"
          style={{
            backgroundColor: color.hex,
          }}
        />
      </div>
    </div>
  );
}
