from pygments.formatter import Formatter


class TextFormatter(Formatter):

    def __init__(self, text, **options):
        super(TextFormatter, self).__init__(**options)
        self.text = text
        self._start = "1.0"
        self._end = "end"
        self._styles = dict(self.style)
        self._highlight_tags = set()
        self.init_tags()

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    def init_tags(self):
        print(self.style)
        self._highlight_tags = set()
        for token, style in self._styles.items():
            if style["color"] is not None:
                self.text.tag_config(str(token), foreground="#{}".format(style["color"]))
                self._highlight_tags.add(str(token))

    def clear_tags(self, start, end="end"):
        for tag in self._highlight_tags:
            self.text.tag_remove(tag, start, end)

    def format(self, tokensource, outfile):
        self.clear_tags("1.0")
        chars = 0
        cumulative_chars = 0
        last_color = None
        last_type = None
        for ttype, value in tokensource:

            while ttype not in self._styles:
                ttype = ttype.parent

            color = self._styles[ttype]['color']
            if color == last_color and color is not None:
                cumulative_chars += len(value)
            elif color != last_color:
                if last_color is not None:
                    start = f"{self._start}+{chars}c"
                    end = f"{self._start}+{chars + cumulative_chars}c"
                    self.text.tag_add(str(last_type), start, end)
                if color is None:
                    chars += cumulative_chars + len(value)
                    cumulative_chars = 0
                else:
                    chars += cumulative_chars
                    cumulative_chars = len(value)
            else:
                chars += len(value)
            last_color = color
            last_type = ttype

        # highlight any remaining text
        if cumulative_chars:
            start = f"{self._start}+{chars}c"
            end = f"{self._start}+{chars + cumulative_chars}c"
            self.text.tag_add(str(last_type), start, end)
