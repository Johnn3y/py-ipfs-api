# -*- coding: utf-8 -*-
from __future__ import absolute_import

from . import base

from .. import multipart

class Section(base.SectionBase):

	@base.returns_single_item
	def put(self, file,input_enc="json",format="cbor",pin=False,hash="sha2-256",**kwargs):
		"""Stores input as a DAG object and returns its key.

		.. code-block:: python

			>>> client.dag.put(io.BytesIO(b'''
			...       {
			...           "Data": "another",
			...           "Links": [ {
			...               "Name": "some link",
			...               "Hash": "QmXg9Pp2ytZ14xgmQjYEiHjVjMFXzCV … R39V",
			...               "Size": 8
			...           } ]
			...       }'''))
			{'Cid': {'/': 'zdpuArYMhkXePWXzQuNMdvpU1YjSX798QtRW9mjAUWDhYTWDq'}}

		Parameters
		----------
		format : str
			Format that the object will be added as. Default: cbor.
		input-enc : str
		    Format that the input object will be. Default: json.
		pin : bool
			Pin this object when adding. Default: False.
		hash : str
			Hash function. Default: sha2-256.


		Returns
		-------
			dict : Cid of the created DAG object
		"""
		
		opts={"input-enc":input_enc,"format":format,"pin":0}
		kwargs.setdefault("opts",{}).update(opts)
		body, headers = multipart.stream_files(file, self.chunk_size)
		return self._client.request('/dag/put', decoder='json', data=body,
		                            headers=headers, **kwargs)
	
	@base.returns_single_item
	def get(self,cid,**kwargs):
		"""Fetches a dag node from ipfs.

		.. code-block:: python

			>>> client.dag.get("zdpuArYMhkXePWXzQuNMdvpU1YjSX798QtRW9mjAUWDhYTWDq")
			{'Data': 'another', 'Links': [{'Hash': 'QmXg9Pp2ytZ14xgmQjYEiHjVjMFXzCVVEcRTWJBmLgR39V', 'Name': 'some link', 'Size': 8}]}


		Parameters
		----------
		Cid : str
			Cid

		Returns
		-------
			dict : DAG node
		"""

		args = (str(cid),)
		return self._client.request('/dag/get',args, decoder='json', **kwargs)
