# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 17:14:23 2019

@author: smorandv
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def rm_ext_and_nan(CTG_features, extra_feature):
    """

    :param CTG_features: Pandas series of CTG features
    :param extra_feature: A feature to be removed
    :return: A dictionary of clean CTG called c_ctg
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    # c_ctg = CTG_features.copy()
    # c_ctg.drop(extra_feature,axis=1).dropna(how='all')
    c_ctg = CTG_features.copy()
    c_ctg = c_ctg.drop(extra_feature, axis=1)
    c_ctg.loc[:, 'LB':'Tendency'] = c_ctg.loc[:, 'LB':'Tendency'].replace('--', np.nan).replace('#', np.nan).replace(
        'Nan', np.nan)
    c_ctg = c_ctg.dropna()

    # --------------------------------------------------------------------------
    return c_ctg


def nan2num_samp(CTG_features, extra_feature):
    """

    :param CTG_features: Pandas series of CTG features
    :param extra_feature: A feature to be removed
    :return: A pandas dataframe of the dictionary c_cdf containing the "clean" features
    """
    c_cdf = {}
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    c_cdf = CTG_features.copy()
    c_cdf = c_cdf.drop(extra_feature, axis=1)
    c_cdf.loc[:, 'LB':'Tendency'] = c_cdf.loc[:, 'LB':'Tendency'].replace('--', np.nan).replace('#', np.nan).replace(
        'Nan', np.nan)
    for i in c_cdf.keys():
        for j in range(1, len(c_cdf)):
            if np.isnan(c_cdf.loc[j, i]):
                c_cdf.loc[j, i] = np.random.choice(c_cdf.loc[:, i].to_list())


    # -------------------------------------------------------------------------

    return pd.DataFrame(c_cdf)


def sum_stat(c_feat):
    """

    :param c_feat: Output of nan2num_cdf
    :return: Summary statistics as a dicionary of dictionaries (called d_summary) as explained in the notebook
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    c = c_feat.describe().to_dict()
    for i in c.keys():
        #     print(c[i])
        c[i].pop('mean')
        c[i].pop('std')
        c[i].pop('count')
        c[i]['Q1'] = c[i].pop('25%')
        c[i]['median'] = c[i].pop('50%')
        c[i]['Q3'] = c[i].pop('75%')
        c[i]['max'] = c[i].pop('max')
    d_summary = c
    # -------------------------------------------------------------------------
    return d_summary


def rm_outlier(c_feat, d_summary):
    """

    :param c_feat: Output of nan2num_cdf
    :param d_summary: Output of sum_stat
    :return: Dataframe of the dictionary c_no_outlier containing the feature with the outliers removed
    """
    c_no_outlier = {}
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    c = c_feat.copy()
    IQR = {}
    low_bound = {}
    high_bound = {}
    for i in c.keys():
        IQR[i] = d_summary[i]['Q3'] - d_summary[i]['Q1']
        low_bound[i] = d_summary[i]['Q1'] - 1.5 * IQR[i]
        high_bound[i] = d_summary[i]['Q3'] + 1.5 * IQR[i]
        for j in range(1, len(c_feat)):
            if c.loc[j, i] < low_bound[i] or c.loc[j, i] > high_bound[i]:
                c.loc[j, i] = np.nan
    c_no_outlier = c
    # -------------------------------------------------------------------------
    return pd.DataFrame(c_no_outlier)


def phys_prior(c_cdf, feature, thresh):
    """

    :param c_cdf: Output of nan2num_cdf
    :param feature: A string of your selected feature
    :param thresh: A numeric value of threshold
    :return: An array of the "filtered" feature called filt_feature
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:-----------------------------
    filt_feature = c_cdf.copy()
    for i in range(1, len(filt_feature)):
        if filt_feature[feature][i] > thresh:
            filt_feature[feature][i] = np.nan
    filt_feature.dropna()
    # -------------------------------------------------------------------------
    return filt_feature


def norm_standard(CTG_features, selected_feat=('LB', 'ASTV'), mode='none', flag=False):
    """

    :param CTG_features: Pandas series of CTG features
    :param selected_feat: A two elements tuple of strings of the features for comparison
    :param mode: A string determining the mode according to the notebook
    :param flag: A boolean determining whether or not plot a histogram
    :return: Dataframe of the normalized/standardazied features called nsd_res
    """
    x, y = selected_feat
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    c = CTG_features.describe().to_dict()
    cc = CTG_features.copy()
    if mode == 'standard':
        for i in cc.keys():
            cc[i] = (cc[i] - c[i]['mean'])/c[i]['std']
    if mode == 'MinMax':
        for i in cc.keys():
            cc[i] = (cc[i] - c[i]['min'])/(c[i]['max']-c[i]['min'])
    if mode == 'mean':
        for i in cc.keys():
            cc[i] = (cc[i] - c[i]['mean'])/(c[i]['max']-c[i]['min'])
    if flag == True:
        xlbl = ['beats/min','%']
        t = [x,y]
        axarr = cc.hist(column=[x,y], bins=100,layout = (2, 1),figsize=(20, 10))
        for i,ax in enumerate(axarr.flatten()):
            ax.set_xlabel(xlbl[i])
            ax.set_ylabel('count')
            ax.set_title(t[i])

    nsd_res = cc
    # -------------------------------------------------------------------------
    return pd.DataFrame(nsd_res)
