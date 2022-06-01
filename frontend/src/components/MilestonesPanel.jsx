import { 
    Table,
    Thead,
    Tbody,
    Tfoot,
    Tr,
    Th,
    Td,
    TableCaption,
    TableContainer,Text, Heading, } from "@chakra-ui/react"
import React, { useState } from "react";

const MilestonesPanel = () => {

    const [testValues, setTestValues] = useState(
        {
            text: "Milestones Overview"
        }
    )

    return (
        <>
            <Text size='lg' fontWeight='bold' mb='2' color='black'>
                <Heading size='md' fontWeight='bold'>Milestones</Heading>
                <TableContainer>
  <Table variant='striped' colorScheme='blue'>
    <TableCaption>Employees Overview</TableCaption>
    <Thead>
      <Tr>
        <Th>Milestone</Th>
        <Th>Status</Th>
        
      </Tr>
    </Thead>
    <Tbody>
      <Tr>
        <Td>1. Milestone</Td>
        <Td>Done</Td>
       
      </Tr>
      <Tr>
        <Td>2. Milestone</Td>
        <Td>Done</Td>
        
      </Tr>
      <Tr>
        <Td>3. Milestone</Td>
        <Td>in Progress</Td>
        
      </Tr>
      <Tr>
        <Td>4. Milestone</Td>
        <Td>Open</Td>
        
      </Tr>
      <Tr>
        <Td>5. Milestone</Td>
        <Td>Open</Td>
        
      </Tr>
    </Tbody>
    
  </Table>
</TableContainer>
                
            </Text>
        </>
    )
}

export default MilestonesPanel