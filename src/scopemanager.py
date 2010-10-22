class Scope( object ):
    stack = []

    @classmethod
    def reset( cls ):
        cls.stack = []

    @classmethod
    def add( cls, step ):
        if cls.stack and cls.stack[ -1 ] == indentation_level:
            return

        cls.stack.append( step )

    @classmethod
    def unindent_until( cls, indentation_level ):
        i = 0
        while cls.stack:
            if cls.stack[-1][3] <= indentation_level:
                break

            i += 1
            cls.indentation_stack.pop()