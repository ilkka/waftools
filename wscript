# -*- python -*-
# encoding: utf-8

import unittestw, Options

top = '.'
out = 'build'

def set_options(opt):
    opt.tool_options('unittest')
    opt.sub_options('test')

def configure(conf):
    conf.check_tool('unittest')
    conf.sub_config('test')

def build(bld):
    bld.add_subdirs('test')
    bld.add_post_fun(unittestw.summary)
    Options.options.all_tests = True
