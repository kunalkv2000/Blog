import React from "react";

function BlogCard({ post, onClick }) {
    const truncateText = (text, maxLength) => {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + "...";
    };

    return (
        <article
            onClick={onClick}
            className="bg-white rounded-2xl shadow-sm border border-slate-200 hover:shadow-lg hover:border-slate-300 transition-all duration-300 cursor-pointer overflow-hidden group"
        >
            {/* Featured Image */}
            <div className="relative h-56 overflow-hidden">
                <img
                    src={`https://ui-avatars.com/api/?name=${encodeURIComponent(post.title)}&size=800&background=random`}
                    alt={post.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
            </div>

            {/* Card Body */}
            <div className="p-5">
                {/* Title */}
                <h2 className="text-xl font-bold text-slate-900 mb-2 line-clamp-2 break-words group-hover:text-sky-600 transition-colors">
                    {post.title}
                </h2>

                {/* Excerpt */}
                <p className="text-slate-600 text-sm mb-4 line-clamp-3 break-words leading-relaxed">
                    {truncateText(post.content, 150)}
                </p>

                {/* Author Info */}
                <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                    <div className="flex items-center gap-3">
                        {/* Avatar */}
                        <img
                            src={`https://ui-avatars.com/api/?name=Admin&background=random&color=fff&size=128`}
                            alt="Author"
                            className="w-9 h-9 rounded-full ring-2 ring-slate-100"
                        />
                        <div>
                            <p className="text-sm font-semibold text-slate-900">
                                Admin
                            </p>
                            <p className="text-xs text-slate-500">
                                {post.created_at
                                    ? new Date(post.created_at).toLocaleDateString('en-US', {
                                        month: 'short',
                                        day: 'numeric',
                                        year: 'numeric'
                                    })
                                    : ""}
                            </p>
                        </div>
                    </div>

                    {/* Bookmark Button */}
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            // Add bookmark functionality here
                        }}
                        className="text-slate-400 hover:text-sky-600 transition-colors p-2 hover:bg-sky-50 rounded-full"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                        </svg>
                    </button>
                </div>
            </div>
        </article>
    );
}

export default BlogCard;
