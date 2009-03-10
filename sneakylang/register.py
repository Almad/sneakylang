# -*- coding: utf-8 -*-

from re import compile, UNICODE

from expanders import Expander
from macro_caller import get_macro_name, expand_macro_from_stream

__all__ = ('ExpanderRegister', 'ParserRegister', 'Register', 'RegisterMap')

class RegisterMap(dict):
    """ Register map is dictionary holding macro : register_with_allowed_macros pair """
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        for k in self:
            self.__after_add(k)

        self.hooks = {}

    def __after_add(self, k):
        self[k].visit_register_map(self)

    def __setitem__(self, k, v):
        dict.__setitem__(self, k,v)
        self.__after_add(k)

    def add_hooks(self, hooks):
        for hook in hooks:
            if hook.macro:
                if not self.hooks.has_key(hook.macro):
                    self.hooks[hook.macro] = set()
                self.hooks[hook.macro].add(hook)

    def pre_hooks(self, stream, macro, builder):
        if macro.__class__ in self.hooks:
            for hook in self.hooks[macro.__class__]:
                stream = hook().pre_macro(stream, macro, builder)
        return stream

    def post_hooks(self, macro, builder):
        if macro.__class__ in self.hooks:
            for hook in self.hooks[macro.__class__]:
                hook().post_macro(macro, builder)

class ParserRegister:
    """ Parser register is holding parsers (aka 'alternative syntaxes') allowed to use for parsing.
    ParserRegister is also responsible for resolving those alternative syntaxes in stream """

    def __init__(self, parsers=None):
        self.parser_start = {}
        #self.parser_start_compiled = {}

        if parsers is not None:
            for parser in parsers:
                self.add(parser)

    def add(self, parser):
        if parser.start is not None:
            for start in parser.start:
                if isinstance(start, str):
                    start = start.decode('utf-8')
                self.parser_start[start] = (compile(u''.join([u'^', start]), flags=UNICODE), parser)
                #self.parser_start_compiled[compile(''.join(['^', start]))] = parser

    def get_parser(self, regexp):
        try:
            return self.parser_start[regexp][1]
        except KeyError:
            raise ValueError('No Parser in register starting with %s' % regexp)

    def _most_matching(self, matching):
        """ Return most matching parser and chunk on which it's resolved """
        most = None
        length = 0
        for m in matching:
            if len(m.string[m.start():m.end()]) > length:
                most = m
                length = len(m.string[m.start():m.end()])
        if most is None:
            return (None, None)
        return (self.parser_start[most.re.pattern[1:]][1], most.string[most.start():most.end()])

    def resolve_parser(self, stream, register, whole_stream=None):
        """ Resolve parser stream.
        Return properly initialized parser or None
        """
	if whole_stream is None:
            whole_stream = stream

	matching = []
	for start in self.parser_start:
            compiled, parser = self.parser_start[start]
            if start.find('^') != -1:
		if compiled.match(whole_stream):
                    matching.append(compiled.match(whole_stream))
            else:
                if compiled.match(stream):
                    matching.append(compiled.match(stream))
        #matching = [parser_start.match(stream) for parser_start in self.parser_start_compiled if parser_start.match(stream)]
        if len(matching) == 0:
            return None
        parser, chunk = self._most_matching(matching)
        if parser is None or chunk is None:
            return None
        return parser(stream, self, chunk, register)

class Register:
    def __init__(self, macro_list=None, parsers=None):
        self.register_map = None
        self.macro_map = {}

        self.parser_register = ParserRegister()

        if macro_list is not None:
            self.add_macros(macro_list)

        if parsers is not None:
            self.add_parsers(parsers)

    def add_macro(self, macro):
        if self.macro_map.has_key(macro.name):
            raise ValueError, 'Macro %s already added under name %s' % (self.macro_map[macro.name], macro.name)
        self.macro_map[macro.name] = macro

    def add_macros(self, macro_list):
        for p in macro_list:
            self.add(p)

    def add(self, macro):
        """ Backward-compatibility symlink, use add_macro instead """
        self.add_macro(macro)

    def add_parsers(self, parsers):
        for parser in parsers:
            self.add_parser(parser)

    def add_parser(self, parser):
        if parser.macro.name in self.macro_map:
            self.parser_register.add(parser)

    def visit_register_map(self, register_map):
        self.register_map = register_map

    def get_macro(self, name):
        try:
            return self.macro_map[name]
        except KeyError:
            raise ValueError, 'No macro parser registered under name %s in registry' % name

    def resolve_parser_macro(self, stream):
        """ Try resolving parser in macro syntax.
        Return properly initialized parser or None
        """
#        logging.debug('Trying to resolve macro in stream')
        try:
            if not isinstance(stream, unicode):
                raise TypeError("Stream expected to be unicode string, %s instead (stream: %s)" % (type(stream), stream))
            return self.macro_map[get_macro_name(stream, self)]
        except KeyError:
#            logging.debug('Macro name %s not in my macro_map' % get_macro_name(stream,self))
            return None
        else:
            raise NotImplementedError,('Unexpected condition, please report this as bug')

    def resolve_macro(self, stream, builder, state=None, whole_stream=None):

        # backward compatibility for tests
        if isinstance(stream, str):
            stream = stream.decode('utf-8')

        if whole_stream is None:
            whole_stream = stream

        parser = self.parser_register.resolve_parser(stream, self, whole_stream)
        if parser is not None:
            # Macro resolved in alternate syntax, use parser to get macro
            macro, stream_new = parser.get_macro(builder, state)
            return (macro, stream_new)

        # resolve in macro syntax
        macro = self.resolve_parser_macro(stream)

        if macro is not None:
            return expand_macro_from_stream(stream, self, builder, state)

        return (None, None)

class ExpanderRegister:
    def __init__(self, expander_map):
        self.expander_map = {}
        for k in expander_map:
            if not isinstance(expander_map[k], Expander):
                raise ValueError('%s must be instance of Expander' % expander_map[k])
            self.expander_map[k] = expander_map[k]

    def get(self, node, format='xhtml11'):
        try:
            return self.expander_map[format][node]
        except KeyError:
            raise ValueError('Expander for format %s for node %s not in registry' % (format, node))
