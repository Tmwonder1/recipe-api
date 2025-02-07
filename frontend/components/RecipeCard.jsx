import { StarIcon } from "@heroicons/react/24/solid";

export default function RecipeCard({ recipe }) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-4 hover:shadow-xl transition-shadow">
      <img 
        src={recipe.image || "https://via.placeholder.com/300x200"} 
        alt={recipe.name} 
        className="w-full h-48 object-cover rounded-lg"
      />
      <h3 className="text-xl font-bold mt-2">{recipe.name}</h3>
      <p className="text-gray-600">{recipe.cuisine}</p>
      <div className="flex items-center mt-2">
        {[1, 2, 3, 4, 5].map((star) => (
          <StarIcon
            key={star}
            className={`h-5 w-5 ${star <= recipe.average_rating ? "text-yellow-400" : "text-gray-300"}`}
          />
        ))}
      </div>
    </div>
  );
}
