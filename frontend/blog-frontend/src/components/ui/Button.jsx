import React from "react";
export default function Button({
  variant = "primary",
  size = "md",
  className = "",
  children,
  ...props
}) {
  const variants = {
    primary: "bg-sky-600 hover:bg-sky-700 text-white",
    secondary: "bg-slate-200 hover:bg-slate-300 text-slate-700",
    danger: "border border-red-300 text-red-600 hover:bg-red-50",
    outline: "border border-slate-300 hover:bg-slate-100 text-slate-700",
    link: "text-slate-600 hover:text-slate-800",
    newbtn: "bg-green-600 hover:bg-green-700 text-white",
    success: "bg-green-600 hover:bg-green-700 text-white",
    warning: "bg-yellow-500 hover:bg-yellow-600 text-black",
    delete: "bg-red-600 hover:bg-red-700 text-white",
    none: "bg-transparent hover:bg-transparent text-inherit",
  };

  const sizes = {
    md: "px-4 py-2 text-sm rounded-lg",
    sm: "px-2 py-1 text-[11px] rounded",
  };

  const variantClass = variants[variant] || variants.primary;
  const sizeClass = sizes[size] || sizes.md;

  return (
    <button
      className={`${variantClass} ${sizeClass} ${className}`.trim()}
      {...props}
    >
      {children}
    </button>
  );
}
