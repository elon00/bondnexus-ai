from pyteal import *

def approval_program():
    box_security_key = Bytes("sec_config")
    is_app_admin = Txn.sender() == App.globalGet(Bytes("admin"))

    @Subroutine(TealType.none)
    def issue_security():
        return Seq([
            Assert(is_app_admin),
            Assert(Txn.assets.length() == Int(1)),
            Approve()
        ])

    @Subroutine(TealType.none)
    def dispatch_coupon():
        return Seq([
            Assert(App.box_extract(box_security_key, Int(0), Int(8)) != Bytes("")),
            Approve()
        ])

    program = Cond(
        [Txn.application_id() == Int(0), Approve()],
        [Txn.on_completion() == OnComplete.OptIn, Approve()],
        [Txn.application_args[0] == Bytes("issue"), issue_security()],
        [Txn.application_args[0] == Bytes("coupon"), dispatch_coupon()],
    )
    return program

if __name__ == "__main__":
    print(compileTeal(approval_program(), mode=Mode.Application, version=10))
