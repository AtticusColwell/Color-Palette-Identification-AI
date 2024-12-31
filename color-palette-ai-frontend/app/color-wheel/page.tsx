"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Home } from "lucide-react";
import { supabase } from "./supabaseClient";
import { ColorWheel } from "@components/ColorWheel";
import { UserProfile } from "@components/UserProfile";

interface Color {
  name: string;
  hex: string;
}

const ColorWheelPage = () => {
  const [selectedColor, setSelectedColor] = useState<Color | null>(null);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<any>(null);
  const router = useRouter();

  useEffect(() => {
    const checkSession = async () => {
      const { data: session, error } = await supabase.auth.getSession();

      if (error) {
        console.error("Error fetching session:", error.message);
        router.push("/signup"); // Redirect to signup if an error occurs
        return;
      }

      if (!session?.session) {
        router.push("/signup"); // Redirect if no session
      } else {
        setUser(session.session.user);
      }

      setLoading(false);
    };

    checkSession();
  }, [router]);

  if (loading) {
    return <p>Loading...</p>; // Add a loading spinner or similar UI
  }

  return (
    <div className="min-h-screen w-full bg-gray-50 flex flex-col items-center">
      <nav className="w-full px-6 py-4 bg-white border-b border-gray-200 flex justify-between items-center">
        <button
          onClick={() => router.push("/")} // Navigate to the home page
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-blue-500 to-purple-500 text-white hover:opacity-90 transition-opacity"
        >
          <Home size={20} />
          <span>Color Palette AI</span>
        </button>
        <UserProfile username={user?.email || "Unknown User"} />
      </nav>
      <main className="container mx-auto px-6 py-12 flex items-start gap-8">
        <h1 className="text-2xl font-bold text-gray-800">Welcome to the Color Wheel</h1>
        <ColorWheel onColorSelect={setSelectedColor} />
        <div className="flex-1 p-6 bg-white rounded-lg shadow-lg">
          <h2 className="text-xl font-bold mb-4">Selected Color</h2>
          {selectedColor ? (
            <div className="flex items-center gap-4">
              <div
                className="w-12 h-12 rounded-full"
                style={{ backgroundColor: selectedColor.hex }}
              ></div>
              <div>
                <p className="font-bold text-lg">{selectedColor.name}</p>
                <p className="text-gray-600">{selectedColor.hex}</p>
              </div>
            </div>
          ) : (
            <p className="text-gray-500">Click a color to see details.</p>
          )}
        </div>
      </main>
    </div>
  );
};

export default ColorWheelPage;


