class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag      = tag
        self.value    = value
        self.children = children
        self.props    = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = "" 
        # We could have also formated the key value string this way
        # for key in self.props:
        #     props_html += f' {key}="{self.props[key]}"'
        # return props_html

        # if we make a view of the dictionary (with the items() method),
        # which places each key/value pair in tuples,
        # we can then access each key value directly like this....
        for key, value in self.props.items():
            props_html += f' {key}="{value}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"
            

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


    def __repr__(self):
        return f"(LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode tag member needs to be defined")
        if self.children is None:
            raise ValueError("ParentNode children member cannot be None") 

        # The LeafNode acts as the "base case" in this recursive process. Since it doesn't have children, its to_html() method just returns its own string, and does not make further recursive calls. That’s what stops the recursion as it traverses the tree of nodes.
        children_html = ""
        for node in self.children:
            children_html += node.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

        # We could also do the same as above with the map function this way:
        # html_lst = list(map(lambda node: node.to_html(), self.children))
        # return f"<{self.tag}>{''.join(html_lst)}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode(tag: {self.tag}, children: {self.children}, props: {self.props})"









