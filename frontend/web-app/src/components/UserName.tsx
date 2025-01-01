// import prisma from '@/lib/db';
//
// export default async function UserName() {
//   const userNames = await prisma.users.findMany();
//   console.log(userNames);
//
//   return (
//     <div><h1>Users</h1></div>
//   )
// }
//
import { getUserName } from '@/lib/utils';
import { cookies } from 'next/headers';


export default async function UserName() {
  const cookieStore = cookies();
  const token = cookieStore.get('token')?.value;
  let userInfo = await getUserName(token);
  // console.log(userInfo['name']);
  return (
    <div>
      <h1 className='font-bold'>User: {userInfo['name']}</h1>
    </div>
  )
}

