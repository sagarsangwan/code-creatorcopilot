import SignIn from "@/components/auth/sign-in";
import { SignOut } from "@/components/auth/signout-button";
import { ComponentExample } from "@/components/component-example";
import { auth } from "@/lib/auth";

export default async function Page() {
    const session = await auth()
    console.log(session?.user)
return (
    <div>
        {session?.user ? <SignOut/> : <SignIn/>}
    </div>
)
}