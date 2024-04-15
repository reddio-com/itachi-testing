use starknet::{ContractAddress, ClassHash};


#[starknet::contract]
mod origin {
    use starknet::{get_caller_address, get_contract_address, replace_class_syscall, ClassHash};
    use starknet::ContractAddress;

    #[storage]
    struct Storage {
        owner: ContractAddress,
        value: u128,
    }

    #[constructor]
    fn constructor(ref self: ContractState, _owner: ContractAddress,) {
        self.owner.write(_owner);
    }

    #[external(v0)]
    fn upgrade_class(ref self: ContractState, new_class_hash: ClassHash) -> bool {
        assert(self.owner.read() == get_caller_address(), 'Owner required');
        replace_class_syscall(new_class_hash);
        true
    }

    #[external(v0)]
    fn set_value(ref self: ContractState, _value: u128) {
        self.value.write(_value);
    }

    #[external(v0)]
    fn get_value(self: @ContractState) {
        self.value.read();
    }

    #[external(v0)]
    fn increase_value(ref self: ContractState) {
        self.value.write(self.value.read() + 1);
    }

    #[external(v0)]
    fn get_version(ref self: ContractState) -> u128 {
        return 0;
    }

    #[external(v0)]
    fn revert_base_on_value( ref self: ContractState, _value: u128) {
        assert(_value > 20, 'Value must be greater than 20');
    }
}