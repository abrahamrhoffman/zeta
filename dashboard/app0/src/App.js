import React from 'react';
import { Admin, Resource } from 'react-admin';
import jsonServerProvider from 'ra-data-json-server';
import FunctionsIcon from '@material-ui/icons/Code';
/*
  import { Admin, Resource, EditGuesser } from 'react-admin';
  import { PostList } from './posts';
  import { UserList } from './users';
  import PostIcon from '@material-ui/icons/Code';
  import UserIcon from '@material-ui/icons/Group';
*/

/*
  const dataProvider = jsonServerProvider('http://jsonplaceholder.typicode.com');
*/

const dataProvider = jsonServerProvider('http://127.0.0.1:8444');
const App = () => (
    /*
      :: Zeta API Custom Data Provider ::

      Must be a function with the following signature ::
      const dataProvider = (type, resource, params) => new Promise();
    */
    <Admin dataProvider={dataProvider}>
        <Resource name="functions" icon={FunctionsIcon} />
        {/*
          <Resource name="functions" list={PostList} icon={PostIcon} />
          <Resource name="users" list={UserList} icon={UserIcon} />
        */}
    </Admin>
);

export default App;
