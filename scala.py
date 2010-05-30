# Scala tool for waf
# Copyright (C) 2010 Ilkka Laukkanen <ilkka.laukkanen@gmail.com>
# Licence: GPLv3 or later

import TalkGen, Utils, Task, Configure, Logs

def scala_build(task):
    """Builder method for Scala programs"""
    env = task.env
    bld = task.generator.bld
    src = task.inputs[0]
    cmd = 'echo {0} {1} {2}'.format(env['SCALAC'], env['SCALAC_FLAGS'], src.srcpath(env))
    Logs.debug('Executing scalac: "{0}"'.format(cmd))
    bld.exec_command(cmd)

scala_vardeps = ['SCALAC', 'SCALAC_FLAGS']

class scala_taskgen(TaskGen.task_gen):
    """Task generator class for Scala."""
    def __init__(self, *k, **kw):
        TaskGen.task_gen.__init__(self, *k, **kw)

@TaskGen.feature('scala')
def apply_scalac(self):
    """Apply the Scala compiler"""
    self.source = getattr(self, 'source', None)
    Logs.debug('apply_scalac, sources {0}'.format(self.source))
    for filename in self.to_list(self.source):
        Logs.debug('apply_scalac for "{0}"'.format(filename))
        node = self.path.find_resource(filename)
        if not node: raise Utils.WafError('Cannot find source file "{0}"'.format(filename))
        task = self.create_task('scalac', node, node.change_ext('.class'))
        task.env = self.env
        task.curdirnode = self.path

@Configure.conftest
def scala_detect(conf):
    env = conf.env
    conf.find_program('scalac', var='SCALAC')
    env['SCALAC_FLAGS'] = ''

b = Task.task_type_from_func
cls = b('scalac', scala_build, vars=scala_vardeps)
