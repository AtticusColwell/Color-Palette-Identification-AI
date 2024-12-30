import React from "react";
import { User } from "lucide-react";

interface UserProfileProps {
  username: string;
}

export function UserProfile({ username }: UserProfileProps) {
  return (
    <div className="flex items-center gap-2">
      <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
        <User size={16} className="text-gray-600" />
      </div>
      <span className="text-gray-700">{username}</span>
    </div>
  );
}
