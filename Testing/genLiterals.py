from itertools import product

# components = "xyzw"
components = "rgba"

def gen_literal(name: str, length: int):
    swizzles = ['"' + ''.join(p) + '"' for p in product(components, repeat=length)]
    return f'{name} = Literal[{", ".join(swizzles)}]'

print(gen_literal("Swizzle2", 2))
print()
print(gen_literal("Swizzle3", 3))
print()
print(gen_literal("Swizzle4", 4))
