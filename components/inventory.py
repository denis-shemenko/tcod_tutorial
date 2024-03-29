import tcod as libtcod

from game_messages import Message

class Inventory:
    def __init__(self, capacity):
        self.owner = None
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = []

        if len(self.items) > self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry more. Inventory full!', libtcod.white)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('You pickup the {0}!'.format(item.name), libtcod.blue)
            })

            self.items.append(item)

        return results

    def remove_item(self, item):
        self.items.remove(item)

    def use(self, item_entity, **kwargs):
        results = []

        item_component = item_entity.item

        if item_component is None or item_component.use_function is None:
            results.append({
                'message': Message('The {0} cannot be used'.format(item_entity.name), libtcod.yellow)
            })
        else:
            if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            else:
                kwargs = {**item_component.function_kwargs, **kwargs}
                item_use_results = item_component.use_function(self.owner, **kwargs)

                for i_u_result in item_use_results:
                    if i_u_result.get('item_consumed'):
                        self.remove_item(item_entity)

                results.extend(item_use_results)

        return results

    def drop_item(self, item):
        results = []

        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        results.append({
            'item_dropped': item,
            'message': Message('You dropped the {0}'.format(item.name), libtcod.yellow)
        })

        return results