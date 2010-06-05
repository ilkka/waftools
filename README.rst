========
 README
========

:Info: Some extra waf tools I've written
:Author: Ilkka Laukkanen <ilkka.s.laukkanen@gmail.com>
:License: GPLv3 or later

Usage
=====

To use in a waf project with git, go::

  $ git submodule add git://github.com/ilkka/waftools.git tasks

and in your wscript, add::

  ...
  import os
  from tasks import <whatever>
  ...
  def configure(conf):
    conf.check_tool('scala', tooldir=os.getcwd()+'/tasks')
  ...
  def build(bld):
    b = bld(features='scala', source='whatever.scala')
  ...

