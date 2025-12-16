import React from "react";
import Button from "../../ui/Button";

function PostTable({ posts, onEdit, onDelete, onRefresh }) {
    return (
        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm">
            <div className="flex justify-between items-center mb-3">
                <h2 className="text-xl font-bold">Posts</h2>
                {/* <Button
                    onClick={onRefresh}
                    variant="outline"
                    size="md"
                    className="text-xl"
                >
                    ↻
                </Button> */}
            </div>

            <div className="overflow-auto rounded-lg border border-slate-200">
                <table className="min-w-full text-xs">
                    <thead className="bg-slate-50 border-b border-slate-200">
                        <tr>
                            <th className="px-3 py-2 text-left font-semibold">ID</th>
                            <th className="px-3 py-2 text-left font-semibold">Title</th>
                            <th className="px-3 py-2 text-left font-semibold">Content</th>
                            <th className="px-3 py-2 text-left font-semibold">Created</th>
                            <th className="px-3 py-2 text-right font-semibold">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {posts.length === 0 ? (
                            <tr>
                                <td
                                    colSpan={5}
                                    className="px-3 py-3 text-center text-slate-500"
                                >
                                    No posts.
                                </td>
                            </tr>
                        ) : (
                            posts.map((p, idx) => (
                                <tr
                                    key={p.id}
                                    className={`border-b last:border-b-0 ${idx % 2 === 0 ? "bg-white" : "bg-slate-50"
                                        }`}
                                >
                                    <td className="px-3 py-2 font-mono">#{p.id}</td>
                                    <td className="px-3 py-2">{p.title}</td>
                                    <td className="px-3 py-2 truncate max-w-xs">{p.content}</td>
                                    <td className="px-3 py-2 text-slate-500">
                                        {p.created_at
                                            ? new Date(p.created_at).toLocaleString()
                                            : ""}
                                    </td>
                                    <td className="px-3 py-2 text-right">
                                        <div className="inline-flex gap-2">
                                            <Button
                                                onClick={() => onEdit(p)}
                                                variant="warning"
                                                size="sm"
                                            >
                                                Edit
                                            </Button>
                                            <Button
                                                variant="delete"
                                                size="sm"
                                                onClick={() => onDelete(p.id)}
                                            >
                                                Delete
                                            </Button>
                                        </div>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default PostTable;
