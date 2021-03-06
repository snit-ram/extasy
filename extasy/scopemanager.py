class _Scope( object ):
    stack = []

    def reset( self ):
        self.stack = []
        
    def get_xpath( self ):
        if not self.stack:
            return ''
        
        return self.stack[ -1 ][ 1 ]
        
    def get_scope_info( self ):
        if not self.stack:
            return None
        
        return self.stack[ -1 ][ 2 ]

    def enter( self, scope_xpath, indentation_level, scope_info = None ):
        if self.stack and self.stack[ -1 ] == indentation_level:
            return

        self.stack.append( ( indentation_level, scope_xpath, scope_info ) )

    def quit_to_indentation_level( self, indentation_level ):
        i = 0
        while self.stack:
            if self.stack[-1][0] <= indentation_level:
                break

            i += 1
            self.stack.pop()
            
scope = _Scope()