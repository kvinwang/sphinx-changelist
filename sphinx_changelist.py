__author__ = 'loong'
__version__ = '0.1.2'

from sphinx.environment import NoUri
from docutils import nodes
from sphinx.util.compat import Directive
from sphinx.directives import other


class change_list(nodes.General, nodes.Element):
    versions = []


class ChangeList(Directive):
    """
    A list of all changes entries.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}

    def run(self):
        node = change_list('')
        node.versions = []
        for line in self.content:
            if not line.strip():
                continue
            if line[0].isspace():
                ver, comment, items = node.versions[-1]
                items.append(line.strip())
            else:
                ver, comment = line.split(' ', 1)
                ver = ver.strip()
                comment = comment.strip()
                node.versions.append((ver, comment, []))
        return [node]


class VersionChange(other.VersionChange):

    def run(self):
        nodes_ = super(VersionChange, self).run()
        if nodes_:
            env = self.state.document.settings.env
            change = nodes_[0]
            change['docname'] = env.docname

            targetid = 'sphinx-changes-%s' % env.new_serialno('sphinx_changes')
            targetnode = nodes.target('', '', ids=[targetid])

            if not hasattr(env, 'changelist_versionchanges'):
                env.changelist_versionchanges = {}

            env.changelist_versionchanges.setdefault(change['version'], []).append((targetnode, change))

            nodes_ = [targetnode] + nodes_

        return nodes_


def process(app, doctree, fromdocname):
    # Replace all changelist nodes with a list of the collected todos.
    # Augment each change with a backlink to the original location.

    env = app.builder.env

    changelists = doctree.traverse(change_list)

    if len(changelists) == 0:
        return

    version_changes = getattr(env, 'changelist_versionchanges', {})

    content = {}

    for version in version_changes:
        for target, change in version_changes[version]:
            para = nodes.line(classes=['changes-source'])

            # Create a reference
            newnode = nodes.reference('', '', internal=True)

            typ = change['type']
            if typ == 'versionchanged':
                para.append(nodes.Text('[Changed] '))
            elif typ == 'versionadded':
                para.append(nodes.Text('[New] '))
            elif typ == 'deprecated':
                para.append(nodes.Text('[Deprecated] '))

            next_node = change.next_node(ascend=True)
            while next_node:
                if isinstance(next_node, nodes.Text):
                    break
                descend = False if isinstance(next_node, nodes.inline) else True
                next_node = next_node.next_node(descend=descend, ascend=True)
            if next_node:
                newnode.append(next_node)

            try:
                newnode['refuri'] = app.builder.get_relative_uri(
                    fromdocname, change['docname'])
                newnode['refuri'] += '#' + target['refid']
            except NoUri:
                # ignore if no URI can be determined, e.g. for LaTeX output
                pass
            para.append(newnode)
            content.setdefault(version, []).append(para)

    for node in changelists:
        sorted_content = []
        for ver, comment, items in node.versions:
            sub_nodes = content.get(ver, [])
            line = '%s %s' % (ver, comment)
            sorted_content.append(nodes.title(line, line))
            for item in items:
                line = nodes.line()
                line.append(nodes.Text(item))
                sorted_content.append(line)
            sorted_content.extend(sub_nodes)

        node.replace_self(sorted_content)


def purge(app, env, docname):
    if not hasattr(env, 'changelist_versionchanges'):
        return
    new_d = {}
    for k in env.changelist_versionchanges:
        for target, change in env.changelist_versionchanges[k]:
            if change['docname'] != docname:
                new_d.setdefault(k, []).append((target, change))
    env.changelist_versionchanges = new_d


def merge(app, env, docnames, other):
    if not hasattr(other, 'changelist_versionchanges'):
        return
    if not hasattr(env, 'changelist_versionchanges'):
        env.changelist_versionchanges = {}
    for k in other.changelist_versionchanges:
        if k in env:
            env[k].extend(other[k])
        else:
            env[k] = other[k]


def setup(app):
    app.add_directive('deprecated', VersionChange)
    app.add_directive('versionadded', VersionChange)
    app.add_directive('versionchanged', VersionChange)

    app.add_directive('changelist', ChangeList)
    app.connect('doctree-resolved', process)
    app.connect('env-purge-doc', purge)
    app.connect('env-merge-info', merge)

    return {'version': '1.0'}
