import React from "react";
import ThemeToggle from "./ThemeToggle";

const Navbar = () => {
  return (
    <nav className="bg-primary text-white dark:bg-dark dark:text-light p-4 flex justify-between">
      <h1 className="text-xl font-bold">TikTok Clone</h1>
      <ThemeToggle />
    </nav>
  );
};

export default Navbar;
