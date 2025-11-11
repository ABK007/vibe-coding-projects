import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { CheckCircle2, ListTodo, Filter, Zap } from "lucide-react";

const Landing = () => {
  const features = [
    {
      icon: ListTodo,
      title: "Organize Everything",
      description: "Create, manage, and track all your tasks in one beautiful interface.",
    },
    {
      icon: Filter,
      title: "Smart Filtering",
      description: "Filter by priority, status, or search to find exactly what you need.",
    },
    {
      icon: Zap,
      title: "Lightning Fast",
      description: "Seamless performance with instant updates and smooth interactions.",
    },
    {
      icon: CheckCircle2,
      title: "Track Progress",
      description: "Mark tasks complete and watch your productivity soar.",
    },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="gradient-bg min-h-screen flex items-center justify-center px-4 py-20">
        <div className="max-w-4xl mx-auto text-center text-white">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 animate-in fade-in slide-in-from-bottom-4 duration-1000">
            Your Tasks, Beautifully Organized
          </h1>
          <p className="text-xl md:text-2xl mb-12 text-white/90 animate-in fade-in slide-in-from-bottom-4 duration-1000 delay-150">
            The elegant todo app that helps you stay focused and get things done
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center animate-in fade-in slide-in-from-bottom-4 duration-1000 delay-300">
            <Button asChild size="lg" className="bg-primary hover:bg-primary/90 text-primary-foreground text-lg px-8 py-6">
              <Link to="/signup">Get Started Free</Link>
            </Button>
            <Button asChild size="lg" variant="outline" className="bg-white/10 hover:bg-white/20 text-white border-white/30 text-lg px-8 py-6 backdrop-blur-sm">
              <Link to="/login">Sign In</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-background">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-4 gradient-text">
            Everything You Need
          </h2>
          <p className="text-xl text-center text-muted-foreground mb-16">
            Powerful features to boost your productivity
          </p>
          
          <div className="grid md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="bg-card rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow border border-border animate-in fade-in slide-in-from-bottom-4"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <feature.icon className="w-12 h-12 text-primary mb-4" />
                <h3 className="text-2xl font-semibold mb-3 text-foreground">
                  {feature.title}
                </h3>
                <p className="text-muted-foreground text-lg">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="gradient-bg py-20 px-4">
        <div className="max-w-4xl mx-auto text-center text-white">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Ready to Get Organized?
          </h2>
          <p className="text-xl mb-8 text-white/90">
            Join thousands of users who are already managing their tasks efficiently
          </p>
          <Button asChild size="lg" className="bg-primary hover:bg-primary/90 text-primary-foreground text-lg px-8 py-6">
            <Link to="/signup">Start Your Journey</Link>
          </Button>
        </div>
      </section>
    </div>
  );
};

export default Landing;
