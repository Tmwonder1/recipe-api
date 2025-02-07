import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";
import RecipeCard from "../components/RecipeCard";

export default function Profile() {
  const [userData, setUserData] = useState(null);
  const [recipes, setRecipes] = useState([]);
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({ username: "", password: "" });
  const navigate = useNavigate();

  // Fetch profile data (existing code)

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      await axios.put(
        "https://your-api-url/profile/update",
        formData,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success("Profile updated!");
      setEditMode(false);
    } catch (error) {
      toast.error("Failed to update profile");
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("file", file);
    
    try {
      const token = localStorage.getItem("token");
      const response = await axios.post(
        "https://your-api-url/profile/upload",
        formData,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setUserData({ ...userData, profile_pic: response.data.profile_pic });
      toast.success("Profile picture updated!");
    } catch (error) {
      toast.error("Failed to upload image");
    }
  };

  return (
    <div className="container mx-auto p-4">
      {/* Profile Header */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="flex items-center gap-6">
          <div className="relative">
            <img
              src={userData?.profile_pic || "https://via.placeholder.com/150"}
              alt="Profile"
              className="w-32 h-32 rounded-full"
            />
            <input
              type="file"
              onChange={handleFileUpload}
              className="absolute inset-0 opacity-0 cursor-pointer"
            />
          </div>
          
          {editMode ? (
            <form onSubmit={handleUpdateProfile} className="flex-1">
              <input
                type="text"
                value={formData.username}
                onChange={(e) => setFormData({...formData, username: e.target.value})}
                className="w-full p-2 border rounded mb-2"
                placeholder="New Username"
              />
              <input
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                className="w-full p-2 border rounded mb-2"
                placeholder="New Password"
              />
              <div className="space-x-4">
                <button type="submit" className="bg-green-500 text-white px-4 py-2 rounded">
                  Save
                </button>
                <button 
                  type="button" 
                  onClick={() => setEditMode(false)}
                  className="bg-gray-500 text-white px-4 py-2 rounded"
                >
                  Cancel
                </button>
              </div>
            </form>
          ) : (
            <div className="flex-1">
              <h1 className="text-3xl font-bold mb-2">{userData?.username}</h1>
              <button
                onClick={() => setEditMode(true)}
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
              >
                Edit Profile
              </button>
            </div>
          )}
        </div>
      </div>

      {/* User Recipes (existing code) */}
    </div>
  );
}
