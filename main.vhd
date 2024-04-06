library IEEE;
use IEEE.STD_LOGIC_1164.all;

entity and_gate is
    port (
        A : in std_logic;
        B : in std_logic;
        C : out std_logic);
end and_gate;

architecture Behavioral of and_gate is
begin
    C <= A and B;
end Behavioral;