import { Link } from "react-router-dom";

export default function Navbar() {
  const token = localStorage.getItem("token");

  return (
    <nav className="bg-gray-800 p-4">
      <div className="container mx-auto flex justify-between">
        <Link to="/" className="text-white text-xl font-bold">
          Recipe App
        </Link>
        <div className="space-x-4">
          {token ? (
            <Link to="/profile" className="text-white">
              Profile
            </Link>
          ) : (
            <Link to="/login" className="text-white">
              Login
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}
