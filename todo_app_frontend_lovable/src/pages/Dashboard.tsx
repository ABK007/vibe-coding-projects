import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { todoApi } from "@/lib/api";
import { Todo, TodoCreate, Priority } from "@/types/todo";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";
import TodoItem from "@/components/TodoItem";
import TodoModal from "@/components/TodoModal";
import { Plus, Search, LogOut, ListTodo, Trash2 } from "lucide-react";

const Dashboard = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editTodo, setEditTodo] = useState<Todo | null>(null);
  const [search, setSearch] = useState("");
  const [filterCompleted, setFilterCompleted] = useState<string>("all");
  const [filterPriority, setFilterPriority] = useState<string>("all");

  useEffect(() => {
    // Check if user is logged in
    const user = localStorage.getItem("user");
    if (!user) {
      navigate("/login");
      return;
    }
    fetchTodos();
  }, [navigate]);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const params: any = {};
      
      if (search) params.search = search;
      if (filterCompleted !== "all") params.completed = filterCompleted === "completed";
      if (filterPriority !== "all") params.priority = filterPriority;
      
      const response = await todoApi.getAll(params);
      setTodos(response.todos);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch todos",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const debounce = setTimeout(() => {
      fetchTodos();
    }, 300);
    return () => clearTimeout(debounce);
  }, [search, filterCompleted, filterPriority]);

  const handleCreateTodo = async (todoData: TodoCreate) => {
    try {
      await todoApi.create(todoData);
      toast({
        title: "Success",
        description: "Todo created successfully",
        className: "bg-success text-success-foreground",
      });
      fetchTodos();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to create todo",
        variant: "destructive",
      });
    }
  };

  const handleUpdateTodo = async (todoData: TodoCreate) => {
    if (!editTodo) return;
    try {
      await todoApi.update(editTodo.id, todoData);
      toast({
        title: "Success",
        description: "Todo updated successfully",
        className: "bg-success text-success-foreground",
      });
      setEditTodo(null);
      fetchTodos();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update todo",
        variant: "destructive",
      });
    }
  };

  const handleToggleTodo = async (id: number) => {
    try {
      await todoApi.toggle(id);
      fetchTodos();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to toggle todo",
        variant: "destructive",
      });
    }
  };

  const handleDeleteTodo = async (id: number) => {
    try {
      await todoApi.delete(id);
      toast({
        title: "Success",
        description: "Todo deleted successfully",
      });
      fetchTodos();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to delete todo",
        variant: "destructive",
      });
    }
  };

  const handleDeleteAllCompleted = async () => {
    try {
      await todoApi.deleteAllCompleted();
      toast({
        title: "Success",
        description: "All completed todos deleted",
      });
      fetchTodos();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to delete completed todos",
        variant: "destructive",
      });
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("user");
    navigate("/");
  };

  const handleEditTodo = (todo: Todo) => {
    setEditTodo(todo);
    setModalOpen(true);
  };

  const handleModalClose = (open: boolean) => {
    setModalOpen(open);
    if (!open) {
      setEditTodo(null);
    }
  };

  const completedCount = todos.filter((t) => t.completed).length;
  const totalCount = todos.length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="gradient-bg text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center">
                <ListTodo className="w-7 h-7 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold">My Todos</h1>
                <p className="text-white/80 text-sm">
                  {completedCount} of {totalCount} completed
                </p>
              </div>
            </div>
            <Button
              variant="ghost"
              onClick={handleLogout}
              className="text-white hover:bg-white/20"
            >
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Actions Bar */}
        <div className="bg-card rounded-xl shadow-md p-6 mb-6">
          <div className="flex flex-col lg:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-5 h-5" />
              <Input
                placeholder="Search todos..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-10 h-11"
              />
            </div>
            <Select value={filterCompleted} onValueChange={setFilterCompleted}>
              <SelectTrigger className="lg:w-[180px] h-11">
                <SelectValue placeholder="Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="active">Active</SelectItem>
                <SelectItem value="completed">Completed</SelectItem>
              </SelectContent>
            </Select>
            <Select value={filterPriority} onValueChange={setFilterPriority}>
              <SelectTrigger className="lg:w-[180px] h-11">
                <SelectValue placeholder="Priority" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Priorities</SelectItem>
                <SelectItem value="low">Low</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="high">High</SelectItem>
              </SelectContent>
            </Select>
            <Button onClick={() => setModalOpen(true)} size="lg" className="h-11">
              <Plus className="w-5 h-5 mr-2" />
              Add Todo
            </Button>
          </div>
          {completedCount > 0 && (
            <div className="mt-4 flex justify-end">
              <Button
                variant="outline"
                onClick={handleDeleteAllCompleted}
                className="text-destructive hover:text-destructive"
              >
                <Trash2 className="w-4 h-4 mr-2" />
                Delete All Completed
              </Button>
            </div>
          )}
        </div>

        {/* Todos List */}
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-primary border-r-transparent"></div>
            <p className="mt-4 text-muted-foreground">Loading todos...</p>
          </div>
        ) : todos.length === 0 ? (
          <div className="bg-card rounded-xl shadow-md p-12 text-center">
            <ListTodo className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">No todos yet</h3>
            <p className="text-muted-foreground mb-6">
              {search || filterCompleted !== "all" || filterPriority !== "all"
                ? "No todos match your filters"
                : "Create your first todo to get started"}
            </p>
            {!search && filterCompleted === "all" && filterPriority === "all" && (
              <Button onClick={() => setModalOpen(true)}>
                <Plus className="w-4 h-4 mr-2" />
                Create Todo
              </Button>
            )}
          </div>
        ) : (
          <div className="space-y-3">
            {todos.map((todo) => (
              <TodoItem
                key={todo.id}
                todo={todo}
                onToggle={handleToggleTodo}
                onEdit={handleEditTodo}
                onDelete={handleDeleteTodo}
              />
            ))}
          </div>
        )}
      </main>

      {/* Todo Modal */}
      <TodoModal
        open={modalOpen}
        onOpenChange={handleModalClose}
        onSave={editTodo ? handleUpdateTodo : handleCreateTodo}
        editTodo={editTodo}
      />
    </div>
  );
};

export default Dashboard;
