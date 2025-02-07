import { useEffect, useState } from "react";
import axios from "axios";
import RecipeCard from "../components/RecipeCard";
import { toast } from "react-hot-toast";

export default function Home() {
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    axios.get("https://your-flask-api.onrender.com/recipes")
      .then((res) => setRecipes(res.data.recipes))
      .catch(() => toast.error("Failed to fetch recipes"));
  }, []);

  return (
    <div className="container mx-auto p-4 grid grid-cols-1 md:grid-cols-3 gap-4">
      {recipes.map((recipe) => (
        <RecipeCard key={recipe.id} recipe={recipe} />
      ))}
    </div>
  );
}
