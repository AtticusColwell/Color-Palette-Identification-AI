"use client";

import React, { useState } from "react";
import { Upload, Camera, ArrowLeft } from "lucide-react"; // Import ArrowLeft for the back button icon
import { useDropzone } from "react-dropzone";
import { useRouter } from "next/navigation"; // Import useRouter for navigation
import { supabase } from "./supabaseClient";

const App: React.FC = () => {
  const router = useRouter(); // Initialize router
  const [formData, setFormData] = useState<{
    firstName: string;
    lastName: string;
    email: string;
    password: string;
    confirmPassword: string;
  }>({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [preview, setPreview] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const onDrop = (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    setPreview(URL.createObjectURL(file));
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: {
      "image/*": [".png", ".jpg", ".jpeg", ".gif"],
    },
    maxFiles: 1,
  });

  const handleCreateAccount = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    const { email, password, confirmPassword } = formData;

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    });

    if (error) {
      setError(error.message);
    } else {
      setSuccess("Account created successfully! Logging you in...");
      // Wait a short time for the session to initialize
      setTimeout(async () => {
        const { data: session, error: sessionError } = await supabase.auth.getSession();
        if (sessionError) {
          setError("Failed to start a session. Please log in manually.");
        } else {
          router.push("/color-wheel"); // Redirect to the ColorWheelPage
        }
      }, 2000); // Allow some buffer for the session to start
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 p-6 md:p-12">
      <div className="relative mx-auto max-w-6xl rounded-xl bg-white p-6 shadow-sm">
        {/* Back Button */}
        <button
          onClick={() => router.push("/")} // Navigate to the homepage
          className="absolute top-4 left-4 flex items-center gap-2 rounded-lg bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200"
        >
          <ArrowLeft size={16} />
          Back
        </button>

        <h1 className="mb-8 text-center text-3xl font-bold text-gray-900">
          Create Your Account
        </h1>
        <div className="grid gap-12 md:grid-cols-2">
          <div>
            <form className="space-y-6" onSubmit={handleCreateAccount}>
              <div className="grid gap-6 md:grid-cols-2">
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    First Name
                  </label>
                  <input
                    type="text"
                    value={formData.firstName}
                    onChange={(e) =>
                      setFormData({ ...formData, firstName: e.target.value })
                    }
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Last Name
                  </label>
                  <input
                    type="text"
                    value={formData.lastName}
                    onChange={(e) =>
                      setFormData({ ...formData, lastName: e.target.value })
                    }
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    required
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Email
                </label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Password
                </label>
                <input
                  type="password"
                  value={formData.password}
                  onChange={(e) =>
                    setFormData({ ...formData, password: e.target.value })
                  }
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Confirm Password
                </label>
                <input
                  type="password"
                  value={formData.confirmPassword}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      confirmPassword: e.target.value,
                    })
                  }
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  required
                />
              </div>
              {error && <p className="text-red-600">{error}</p>}
              {success && <p className="text-green-600">{success}</p>}
              <div className="mt-8 text-center">
                <button
                  type="submit"
                  className="rounded-lg bg-blue-600 px-8 py-3 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  Create Account
                </button>
              </div>
            </form>
          </div>
          <div>
            <div className="mb-6 rounded-lg bg-gray-50 p-4">
              <h3 className="mb-2 text-lg font-medium text-gray-900">
                Photo Requirements
              </h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-center gap-2">
                  <Camera size={16} />
                  Good lighting is essential
                </li>
                <li>Clear view of face, including hair, eyes, and skin</li>
                <li>Neutral background preferred</li>
                <li>Similar to the example shown below</li>
              </ul>
            </div>
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <h4 className="mb-2 text-sm font-medium text-gray-700">
                  Example Photo
                </h4>
                <img
                  src="https://example.com/example-photo.jpg"
                  alt="Example photo"
                  className="h-48 w-full rounded-lg object-contain"
                />
              </div>
              <div>
                <h4 className="mb-2 text-sm font-medium text-gray-700">
                  Your Photo
                </h4>
                <div
                  {...getRootProps()}
                  className="flex h-48 cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 hover:bg-gray-100"
                >
                  <input {...getInputProps()} />
                  {preview ? (
                    <img
                      src={preview}
                      alt="Preview"
                      className="h-full w-full rounded-lg object-cover"
                    />
                  ) : (
                    <div className="text-center">
                      <Upload className="mx-auto h-8 w-8 text-gray-400" />
                      <p className="mt-2 text-sm text-gray-500">
                        Click or drag photo here
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default App;
