#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-07 19:45:15
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from rauth import OAuth2Service
from flask import current_app, redirect


class OAuthSignIn(object):
    """docstring for OAuthSignIn"""
    providers = None

    def __init__(self, providerName):
        self.providerName = providerName
        credentials = current_app.config['OAUTH_CREDENTIALS'][providerName]
        self.consumerId = credentials['id']
        self.consumerSecret = credentials['secret']

    def authorize(self):
        """
        此方法用于将当前页面跳转至用户认证页面，并在完成认证之后，带着从OAUTH服务器获得
        的code转到callbackurl
        """
        pass

    def callback(self,code):
        """
        有了authorize返回的code之后，将code、client_id、client_secret post给OAUTH
        服务器，获得到用以获取用户数据的token
        """
        pass

    def getCallbackURL(self):
        pass

    @classmethod
    def getProvider(cls, providerName):
        if cls.providers is None:
            cls.providers = {}
            for providerClass in cls.__subclasses__():
                provider = providerClass()
                cls.providers[provider.providerName] = provider
        return cls.providers[providerName]


class GithubSigIn(OAuthSignIn):
    """docstring for GithubSigIn"""

    def __init__(self):
        super(GithubSigIn, self).__init__('Github')
        self.service = OAuth2Service(
            name='Github',
            client_id=self.consumerId,
            client_secret=self.consumerSecret,
            authorize_url='https://github.com/login/oauth/authorize',
            access_token_url='https://github.com/login/oauth/access_token',
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='user',
            response_type='code',))

    def callback(self, code):
        if code is None:
            return None, None, None
        oauthSession = self.service.get_auth_session(
            data=dict(code=code,
                      client_id=self.consumerId,
                      client_secret=self.consumerSecret))
        me = oauthSession.get('https://api.github.com/user').json()
        # flash('Logged in as ' + me['name'])
        return me


class BattlenetSignIn(OAuthSignIn):
    """docstring for GithubSigIn"""

    def __init__(self):
        super(BattlenetSignIn, self).__init__('BattleNet')
        self.service = OAuth2Service(
            name='BattleNet',
            client_id=self.consumerId,
            client_secret=self.consumerSecret,
            authorize_url='https://www.battlenet.com.cn/oauth/authorize',
            access_token_url='https://www.battlenet.com.cn/oauth/token',
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            client_id=self.consumerId,
            response_type='code',
            redirect_uri='https://localhost:5000/callback/BattleNet'))

    def callback(self, code):
        if code is None:
            return None, None, None
        '''
        战网的返回数据需要json.loads当做decoder,也就是说需要在rauth.service中增加json的
        decoder
        '''
        oauthSession = self.service.get_auth_session(
            data=dict(code=code,
                      client_id=self.consumerId,
                      client_secret=self.consumerSecret,
                      grant_type='authorization_code',
                      redirect_uri='https://localhost:5000/callback/BattleNet'))
        me = oauthSession.get(
            'https://api.battlenet.com.cn/account/user').json()
        # flash('Logged in as ' + me['name'])
        return me

