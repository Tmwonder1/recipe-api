import { Link } from "react-router-dom";

export default function UserCard({ user }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-4">
      <img 
        src={user.profile_pic || "https://via.placeholder.com/100"} 
        alt={user.username}
        className="w-24 h-24 rounded-full mx-auto mb-4"
      />
      <h3 className="text-center font-bold">{user.username}</h3>
      <div className="flex justify-center mt-4">
        <Link 
          to={`/users/${user.id}`} 
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          View Profile
        </Link>
      </div>
    </div>
  );
}
