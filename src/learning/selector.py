import learning.ols as ols
import learning.lasso as lasso
import learning.sgd as sgd
import learning.ridge as ridge
import learning.tree as tree
import logging as log


def regression_tree_supplier(args):
    return tree.Tree(args.arguments)


def ols_regression_supplier(args):
    return ols.Ols(args.arguments)


def ridge_regression_supplier(args):
    return ridge.Ridge(args.arguments)


def sgd_regression_supplier(args):
    return sgd.Sgd(args.arguments)


def lasso_regression_supplier(args):
    return lasso.Lasso(args.arguments)


def select_model_supplier(args):
    case = {
        'ols': ols_regression_supplier,
        'lasso': lasso_regression_supplier,
        'ridge': ridge_regression_supplier,
        'sgd': sgd_regression_supplier,
        'tree': regression_tree_supplier
    }
    select_function = case[args.model]
    log.info('action=selecting-model value=%s' % args.model)
    return select_function


def select_model(args):
    select_function = select_model_supplier(args)
    return select_function(args)
