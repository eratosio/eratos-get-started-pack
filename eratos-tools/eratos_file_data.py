import os
import json
from slugify import slugify

def download_all_files_from_space(adapter = None, space_ern = None,destination = '.'):

        res = adapter.Resource(ern = space_ern)

        if str(res.type()) != 'ern:e-pn.io:schema:space':
            raise ValueError("The provided ERN does not correspond to an Eratos space ERN")

        res_col = adapter.Resource(ern = res.prop('collection'))

        for item in res_col.prop('items'):

            item_res = adapter.Resource(ern = item['ern'])
            print(item_res.prop('name'))
            #print(item_res.data())
            try:
                lst = item_res.data().list_objects()
            except Exception as e:
                print("Could not find data files for: ", item_res.prop('name'))
                print("Will skip and continue")
                continue
            for ob in lst:

                #print(ob)
                if ob['key'].endswith(".nc"):
                    continue
                else:

                    item_res.data().fetch_object(ob['key'], dest=destination)

                    print("Downloaded: ", ob['key'])


def download_files_in_dataset(adapter = None, block_ern = None, destination = '.'):

    item_res = adapter.Resource(ern = block_ern)

    if str(item_res.type()) != 'ern:e-pn.io:schema:block':
        raise ValueError("The provided ERN does not correspond to an Eratos Block ERN")


    print(item_res.prop('name'))
    #print(item_res.data())
    try:
        lst = item_res.data().list_objects()
    except Exception as e:
        print("Could not find data files for: ", item_res.prop('name'))
       
    for ob in lst:

        #print(ob)
        if ob['key'].endswith(".nc"):
            print("Will not download files that can be accessed through the gridded interface", item_res.prop('name'))
            continue
        else:

            item_res.data().fetch_object(ob['key'], dest=destination)

            print("Downloaded: ", ob['key'])
            
def view_all_data_in_space(adapter=None, space_ern=None, show_block_ern=False):
    """
    This function lists all data files in a specified space on the Eratos platform, 
    excluding files with a ".nc" extension. It prints the item names, optionally 
    along with their block ERNs, followed by the file names.

    Args:
    adapter: An instance of the Eratos adapter to interact with the platform.
    space_ern: The ERN (Eratos Resource Name) of the space to be queried.
    show_block_ern: Boolean flag to indicate whether to print the block ERN. Default is True.

    Raises:
    ValueError: If the provided ERN does not correspond to an Eratos space ERN.
    TypeError: If the adapter or space_ern is None.
    """
    if adapter is None:
        raise TypeError("The 'adapter' parameter cannot be None")
    if space_ern is None:
        raise TypeError("The 'space_ern' parameter cannot be None")

    res = adapter.Resource(ern=space_ern)

    if str(res.type()) != 'ern:e-pn.io:schema:space':
        raise ValueError("The provided ERN does not correspond to an Eratos space ERN")

    res_col = adapter.Resource(ern=res.prop('collection'))

    for item in res_col.prop('items'):
        item_res = adapter.Resource(ern=item['ern'])
        item_name = item_res.prop('name')
        block_ern = item['ern']
        if show_block_ern:
            print(f"{item_name} (block_ern: {block_ern}):")
        else:
            print(f"{item_name}:")
        try:
            lst = item_res.data().list_objects()
        except Exception as e:
            print("    Could not find data files for:", item_name)
            print("    Will skip and continue")
            continue

        for ob in lst:
            if not ob['key'].endswith(".nc"):
                print(f"    - {ob['key']}")

