"use client";
import React from "react";
import { LogIn, Palette, Sparkles } from "lucide-react";
import { useRouter } from "next/navigation"; // Import useRouter

const Home: React.FC = () => {
  const router = useRouter(); // Initialize useRouter

  const handleDiscoverClick = () => {
    router.push("/color-wheel"); // Navigate to the color-wheel page
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-500 to-purple-700">
      <nav className="p-6 flex justify-between items-center">
        <div className="text-white text-2xl font-bold flex items-center gap-2">
          <Palette className="h-8 w-8" />
          ColorPaletteAI
        </div>
        <button className="bg-white/10 hover:bg-white/20 text-white px-4 py-2 rounded-lg flex items-center gap-2 backdrop-blur-sm transition-all">
          <LogIn className="h-4 w-4" />
          Sign In
        </button>
      </nav>
      <main className="container mx-auto px-6 py-12 text-center">
        <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
          Discover Your Perfect Color Palette
        </h1>
        <p className="text-xl text-white/90 mb-12 max-w-2xl mx-auto">
          Enhance your appearance and build a wardrobe that truly reflects
          you through personalized color analysis.
        </p>
      </main>
      <section className="container mx-auto px-6 py-12">
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-white">
            <h3 className="text-xl font-bold mb-4">Enhance Your Appearance</h3>
            <p className="text-white/90">
              Discover colors that complement your skin tone, highlight your
              best features, and minimize imperfections.
            </p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-white">
            <h3 className="text-xl font-bold mb-4">
              Build a Cohesive Wardrobe
            </h3>
            <p className="text-white/90">
              Create a versatile collection of clothes that work together
              perfectly, simplifying your daily choices.
            </p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-white">
            <h3 className="text-xl font-bold mb-4">Stay Seasonally Relevant</h3>
            <p className="text-white/90">
              Align your style with seasonal trends while maintaining your
              unique color harmony.
            </p>
          </div>
        </div>
      </section>
      <section className="container mx-auto px-6 py-16 text-center">
        <button
          className="bg-white text-purple-600 hover:bg-white/90 px-8 py-4 rounded-full text-xl font-bold flex items-center gap-2 mx-auto transition-all"
          onClick={handleDiscoverClick} // Attach the click handler
        >
          <Sparkles className="h-5 w-5" />
          Discover Your Color Palette Now
        </button>
      </section>
    </div>
  );
};

export default Home;

