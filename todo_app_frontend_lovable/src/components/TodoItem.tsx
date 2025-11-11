import { Todo } from "@/types/todo";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Badge } from "@/components/ui/badge";
import { Pencil, Trash2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface TodoItemProps {
  todo: Todo;
  onToggle: (id: number) => void;
  onEdit: (todo: Todo) => void;
  onDelete: (id: number) => void;
}

const priorityColors = {
  low: "bg-blue-100 text-blue-800 hover:bg-blue-200",
  medium: "bg-amber-100 text-amber-800 hover:bg-amber-200",
  high: "bg-red-100 text-red-800 hover:bg-red-200",
};

const TodoItem = ({ todo, onToggle, onEdit, onDelete }: TodoItemProps) => {
  return (
    <div className="group bg-card border border-border rounded-lg p-4 shadow-sm hover:shadow-md transition-all">
      <div className="flex items-start gap-3">
        <Checkbox
          checked={todo.completed}
          onCheckedChange={() => onToggle(todo.id)}
          className="mt-1"
        />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <h3
              className={cn(
                "font-semibold text-lg",
                todo.completed && "line-through text-muted-foreground"
              )}
            >
              {todo.title}
            </h3>
            <Badge variant="outline" className={priorityColors[todo.priority]}>
              {todo.priority}
            </Badge>
          </div>
          {todo.description && (
            <p
              className={cn(
                "text-sm text-muted-foreground",
                todo.completed && "line-through"
              )}
            >
              {todo.description}
            </p>
          )}
          <p className="text-xs text-muted-foreground mt-2">
            {new Date(todo.created_at).toLocaleDateString()}
          </p>
        </div>
        <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
          <Button
            size="icon"
            variant="ghost"
            onClick={() => onEdit(todo)}
            className="h-8 w-8"
          >
            <Pencil className="h-4 w-4" />
          </Button>
          <Button
            size="icon"
            variant="ghost"
            onClick={() => onDelete(todo.id)}
            className="h-8 w-8 text-destructive hover:text-destructive"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
};

export default TodoItem;
