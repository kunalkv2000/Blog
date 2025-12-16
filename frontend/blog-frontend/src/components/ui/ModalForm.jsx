import React from "react";
import Button from "./Button";

export default function ModalForm({
  title,
  onSubmit,
  onCancel,
  status,
  submitLabel = "Save",
  cancelLabel = "Cancel",
  children,
  className = "",
}) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/40" onClick={onCancel} />
      <div
        className={`relative bg-white rounded-lg p-6 w-full max-w-lg mx-4 ${className}`}
      >
        <h3 className="text-lg font-semibold mb-3">{title}</h3>
        {status && (
          <div className="mb-2 text-xs text-amber-700 bg-amber-50 border border-amber-200 px-2 py-1 rounded">
            {status}
          </div>
        )}
        <form onSubmit={onSubmit} className="space-y-3 text-sm">
          {children}
          <div className="flex gap-2 justify-end">
            <Button
              type="button"
              variant="secondary"
              onClick={onCancel}
              className="px-3 py-1.5 text-sm"
            >
              {cancelLabel}
            </Button>
            <Button type="submit" className="px-3 py-1.5 text-sm">
              {submitLabel}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
