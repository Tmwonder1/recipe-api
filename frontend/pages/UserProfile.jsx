import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import RecipeCard from "../components/RecipeCard";
import UserCard from "../components/UserCard";

export default function UserProfile() {
  const { userId } = useParams();
  const [user, setUser] = useState(null);
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    axios.get(`https://your-api-url/users/${userId}`)
      .then(res => {
        setUser(res.data.user);
        setRecipes(res.data.recipes);
      })
      .catch(() => toast.error("User not found"));
  }, [userId]);

  if (!user) return <div>Loading...</div>;

  return (
    <div className="container mx-auto p-4">
      <UserCard user={user} />
      <h2 className="text-2xl font-bold my-4">Recipes by {user.username}</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {recipes.map(recipe => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </div>
    </div>
  );
}
