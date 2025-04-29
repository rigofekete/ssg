class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag      = tag
        self.value    = value
        self.children = children
        self.props    = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        props_html = "" 
        # We coould have also formated the key value string this way
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
            

            
