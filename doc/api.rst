API
===

.. note::

    All doctests in this documentation use Python 3.3 syntax.

.. autoclass:: urlobject.URLObject
   :members: from_iri, scheme, with_scheme,
      netloc, with_netloc,
      username, with_username, without_username,
      password, with_password, without_password,
      hostname, with_hostname,
      port, default_port, with_port, without_port,
      auth, with_auth, without_auth,
      path, with_path, root, parent, is_leaf,
      add_path_segment, add_path,
      query, with_query, without_query,
      query_list, query_dict, query_multi_dict,
      add_query_param, add_query_params,
      set_query_param, set_query_params,
      del_query_param, del_query_params, del_query_param_value,
      fragment, with_fragment, without_fragment,
      relative
