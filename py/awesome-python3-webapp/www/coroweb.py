Skip
to
content

Search or jump
to��

Pull
requests
Issues
Marketplace
Explore


@aiguang11211


Sign
out
5
23
26
justoneliu / web_app
Code
Issues
1
Pull
requests
1
Projects
0
Wiki
Insights
web_app / www / webframe.py
0
ae640f
on
30
Jul


@justoneliu


justoneliu
day
5: encapsulate
a
web
frame

217
lines(189
sloc)  8.57
KB
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio, os, inspect, logging, functools

from urllib import parse
from aiohttp import web
from apis import APIError


def get(path):
    ' @getװ����������������URL��HTTP method-GET������ '

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper

    return decorator


def post(path):
    ' @postװ����������������URL��HTTP method-POST������ '

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper

    return decorator


def has_request_arg(fn):
    ' ��麯���Ƿ���request���������ز���ֵ������request���������ò����Ƿ�Ϊ�ú��������һ�������������׳��쳣 '
    params = inspect.signature(fn).parameters  # ���� ������������ ����Ϣ
    found = False
    for name, param in params.items():
        if name == 'request':
            found = True
            continue  # �˳�����ѭ��
        # ����ҵ���request�������󣬻�����λ�ò������ͻ��׳��쳣
        if found and (
                param.kind != inspect.Parameter.VAR_POSITIONAL and param.kind != inspect.Parameter.KEYWORD_ONLY and param.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError(
                'request parameter must be the last named parameter in function: %s%s' % (fn.__name__, str(sig)))
    return found


def has_var_kw_arg(fn):
    ' ��麯���Ƿ��йؼ��ֲ����������ز���ֵ '
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True


def has_named_kw_args(fn):
    ' ��麯���Ƿ��������ؼ��ֲ��������ز���ֵ '
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            return True


def get_named_kw_args(fn):
    ' ���������е� �����ؼ��ֲ����� ��Ϊһ��tuple���� '
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)


def get_required_kw_args(fn):
    ' ���������� ûĬ��ֵ�� �����ؼ��ֲ����� ��Ϊһ��tuple���� '
    args = []
    params = inspect.signature(
        fn).parameters  # An ordered mapping of parameters' names to the corresponding Parameter object.
    for name, param in params.items():

        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            # param.kind : describes how argument values are bound to the parameter.
            # KEYWORD_ONLY : value must be supplied as keyword argument, which appear after a * or *args
            # param.default : the default value for the parameter,if has no default value,this is set to Parameter.empty
            # Parameter.empty : a special class-level marker to specify absence of default values and annotations
            args.append(name)
    return tuple(args)


class RequestHandler(object):
    ' ����������������װ������ '

    def __init__(self, app, fn):
        # app : an application instance for registering the fn
        # fn : a request handler with a particular HTTP method and path
        self._app = app
        self._func = fn
        self._has_request_arg = has_request_arg(fn)  # ��麯���Ƿ���request����
        self._has_var_kw_arg = has_var_kw_arg(fn)  # ��麯���Ƿ��йؼ��ֲ�����
        self._has_named_kw_args = has_named_kw_args(fn)  # ��麯���Ƿ��������ؼ��ֲ���
        self._named_kw_args = get_named_kw_args(fn)  # ���������е� �����ؼ��ֲ����� ��Ϊһ��tuple����
        self._required_kw_args = get_required_kw_args(fn)  # ���������� ûĬ��ֵ�� �����ؼ��ֲ����� ��Ϊһ��tuple����

    async def __call__(self, request):
        ' ��������request handler,must be a coroutine that accepts a request instance as its only argument and returns a streamresponse derived instance '
        kw = None
        if self._has_var_kw_arg or self._has_named_kw_args or self._required_kw_args:
            # ������Ĵ��������� �ؼ��ֲ����� �� �����ؼ��ֲ��� �� request����
            if request.method == 'POST':
                # POST����Ԥ����
                if not request.content_type:
                    # ������������Ϣʱ����
                    return web.HTTPBadRequest('Missing Content-Type.')
                ct = request.content_type.lower()
                if ct.startswith('application/json'):
                    # ����JSON���͵����ݣ���������ֵ���
                    params = await request.json()
                    if not isinstance(params, dict):
                        return web.HTTPBadRequest('JSON body must be object.')
                    kw = params
                elif ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
                    # ��������͵����ݣ���������ֵ���
                    params = await request.post()
                    kw = dict(**params)
                else:
                    # �ݲ�֧�ִ��������������͵�����
                    return web.HTTPBadRequest('Unsupported Content-Type: %s' % request.content_type)
            if request.method == 'GET':
                # GET����Ԥ����
                qs = request.query_string
                # ��ȡURL�е������������ name=Justone, id=007
                if qs:
                    # �����������������ֵ���
                    kw = dict()
                    for k, v in parse.parse_qs(qs, True).items():
                        # parse a query string, data are returned as a dict. the dict keys are the unique query variable names and the values are lists of values for each name
                        # a True value indicates that blanks should be retained as blank strings
                        kw[k] = v[0]
        if kw is None:
            # �������������ʱ
            kw = dict(**request.match_info)
        # Read-only property with AbstractMatchInfo instance for result of route resolving
        else:
            # �����ֵ��ռ��������
            if not self._has_var_kw_arg and self._named_kw_args:
                copy = dict()
                for name in self._named_kw_args:
                    if name in kw:
                        copy[name] = kw[name]
                kw = copy
            for k, v in request.match_info.items():
                if k in kw:
                    logging.warning('Duplicate arg name in named arg and kw args: %s' % k)
                kw[k] = v
        if self._has_request_arg:
            kw['request'] = request
        if self._required_kw_args:
            # �ռ���Ĭ��ֵ�Ĺؼ��ֲ���
            for name in self._required_kw_args:
                if not name in kw:
                    # �����ڹؼ��ֲ���δ����ֵʱ���أ����� һ����˺�ע��ʱ��û����������ύע������ʱ����ʾ����δ����
                    return web.HTTPBadRequest('Missing arguments: %s' % name)
        logging.info('call with args: %s' % str(kw))
        try:
            r = await self._func(**kw)
            # �����ô��������������������������������
            return r
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)


def add_static(app):
    ' ��Ӿ�̬��Դ·�� '
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')  # ��ð���'static'�ľ���·��
    # os.path.dirname(os.path.abspath(__file__)) ���ؽű�����Ŀ¼�ľ���·��
    app.router.add_static('/static/', path)  # ��Ӿ�̬��Դ·��
    logging.info('add static %s => %s' % ('/static/', path))


def add_route(app, fn):
    ' ��������ע�ᵽweb��������·�ɵ��� '
    method = getattr(fn, '__method__', None)  # ��ȡ fn �� __method__ ���Ե�ֵ������ΪNone
    path = getattr(fn, '__route__', None)  # ��ȡ fn �� __route__ ���Ե�ֵ������ΪNone
    if path is None or method is None:
        raise ValueError('@get or @post not define in %s.' % str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        # ������������Э��ʱ����װΪЭ�̺���
        fn = asyncio.coroutine(fn)
    logging.info(
        'add route %s %s => %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method, path, RequestHandler(app, fn))


def add_routes(app, module_name):
    ' �Զ���handlerģ����������ĺ���ע�� '
    n = module_name.rfind('.')
    if n == (-1):
        # û��ƥ����ʱ
        mod = __import__(module_name, globals(), locals())
    # importһ��ģ�飬��ȡģ���� __name__
    else:
        # ���ģ������ name������ֵ��mod
        name = module_name[n + 1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    for attr in dir(mod):
        # dir(mod) ��ȡģ����������
        if attr.startswith('_'):
            # �Թ�����˽������
            continue
        fn = getattr(mod, attr)
        # ��ȡ���Ե�ֵ��������һ��method
        if callable(fn):
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                # ���Ѿ����ι���URL������ע�ᵽweb�����·����
                add_route(app, fn)
