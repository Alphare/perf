import ast
import inspect
import time

__all__ = ["perfit"]


def perfit(func):
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        val = func(*args, **kwargs)
        end = time.monotonic()
        print(start - end)
        return val

    return wrapper


class Timed(ast.NodeTransformer):
    start_timer = ast.parse("s = time.monotonic()").body[0]
    end_timer = ast.parse("e = time.monotonic()").body[0]
    print_timer = ast.parse("print(e - s, file = __buffer)").body[0]
    
    def visit_FunctionDef(self, node):
        node.decorator_list = list(
            filter(lambda decorator: decorator.id != "analyze", node.decorator_list)
        )
        
        fake_body = node.body.copy()
        for n, _node in enumerate(node.body):
            if isinstance(_node, ast.Expr):
                n = fake_body.index(_node)
                fake_body.insert(n , self.start_timer)
                fake_body.insert(n + 2, self.end_timer)
                fake_body.insert(n + 3, self.print_timer)
        
        node.body.insert(0, *ast.parse("import time").body)
        node.body = fake_body

        return self.generic_visit(node)
    def visit_expr(self, node):
        print(node)
        return node

def analyze(buf):
    def wrapper(func):
        source = inspect.getsource(func)
        tree = ast.parse(source)
        tree = Timed().visit(tree)
        ast.fix_missing_locations(tree)
        
        code = compile(tree, "<perf>", "exec")
        frame = inspect.currentframe().f_back
        exec(compile(tree, "<ast>", "exec"), frame.f_globals, frame.f_locals)
        
        func = frame.f_locals.get(func.__name__)
        
        def __wrapper(*args, **kwargs):
            kwargs["__buf"] = buf
            return func(*args, **kwargs)
        
        return __wrapper
    return wrapper
